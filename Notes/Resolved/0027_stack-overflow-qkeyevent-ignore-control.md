### Notes

-   I encountered an issue where pressing `Ctrl+C` writes a character into the document.
    This was caused because pressing control generates a `keyPressEvent`.

-   I dug into the source code of `QLineEdit` and figured out, how they do it.
    Then I answered a related stack overflow question:

    The accepted answer is unfortunately incomplete. If you press `Ctrl+C`, then `QKeyEvent::text()` will return `"\x03"` (^C "End of Text").
    That is not an empty string.

    I decided to look inside the Qt source code, since they need to handle this problem for `QLineEdit` as well:

    -   In `QLineEdit::keyPressEvent`:

        ```c++
        d->control->processKeyEvent(event);
        ```
        [src/widgets/widgets/qlineedit.cpp:1742][1]

    -   In `QWidgetLineControl::processKeyEvent`:

        ```c++
        if (unknown
            && !isReadOnly()
            && isAcceptableInput(event)) {
            insert(event->text());
        ```
        [src/widgets/widgets/qwidgetlinecontrol.cpp:1912][2]

    -   In `QInputControl::isAcceptableInput`:

        ```c++
        bool QInputControl::isAcceptableInput(const QKeyEvent *event) const
        {
            const QString text = event->text();
            if (text.isEmpty())
                return false;

            const QChar c = text.at(0);

            // Formatting characters such as ZWNJ, ZWJ, RLM, etc. This needs to go before the
            // next test, since CTRL+SHIFT is sometimes used to input it on Windows.
            if (c.category() == QChar::Other_Format)
                return true;

            // QTBUG-35734: ignore Ctrl/Ctrl+Shift; accept only AltGr (Alt+Ctrl) on German keyboards
            if (event->modifiers() == Qt::ControlModifier
                    || event->modifiers() == (Qt::ShiftModifier | Qt::ControlModifier)) {
                return false;
            }

            if (c.isPrint())
                return true;

            if (c.category() == QChar::Other_PrivateUse)
                return true;

            if (c.isHighSurrogate() && text.size() > 1 && text.at(1).isLowSurrogate())
                return true;

            if (m_type == TextEdit && c == u'\t')
                return true;

            return false;
        }
        ```

        [src/gui/text/qinputcontrol.cpp:21][3]

    This is exactly what you need but you may want to change the check for `\t` and ignore that as well.

  [1]: https://github.com/qt/qtbase/blob/7689d4ad2f673317af432aae498da74d13703126/src/widgets/widgets/qlineedit.cpp#L1742
  [2]: https://github.com/qt/qtbase/blob/7689d4ad2f673317af432aae498da74d13703126/src/widgets/widgets/qwidgetlinecontrol.cpp#L1912-L1915
  [3]: https://github.com/qt/qtbase/blob/7689d4ad2f673317af432aae498da74d13703126/src/gui/text/qinputcontrol.cpp#L21-L53

### Results

-   Added `should_ignore_key_event` helper function, inspired from `QInputControl::isAcceptableInput`.

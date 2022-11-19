# Writer

## About

This is a word processor similar to Microsoft Word or LibreOffice Writer.
My goal is to support the core features without getting tied up in details.

I originally started this project because I wanted to add a Writer application to Serenity OS.
Maybe, that will still happen at some point in the future, but I no longer have plans to do so at the moment.

The problem is, that this whole thing is much more challenging than expected.
I thought that I could simply create a wrapper for a web browser and thus use HTML/CSS for rendering.
Then I would write some C++ code that deals with all the interaction logic and connects to LibWeb and the file system.

However, I quickly realized that this would not work, because of paging.
Paging is the process of taking the text and deciding on which page it should be rendered.
This is a chicken-egg problem where the layout can infulence the structure of the page, which itself infuences the layout.

Since CSS is not capable of modifying the DOM and the support for CSS3-REGIONS was removed from browsers, there is no way to get this working.
There are workarounds, but I ultimately decided to create my own rendering engine ditching the web browser entirely.
I stated working on a prototype in Python, which became this project.

## Demo

*This is in an early state of development.
Most of the basic functionality is there but it's extremely buggy and some key features are missing.*

*In the demo, the cursor is sometimes flickering due to a rendering bug that I am working to resolve.*

https://user-images.githubusercontent.com/31994781/192720179-6e014be6-9ca7-4e91-aca0-d2edbc03a5fe.mp4

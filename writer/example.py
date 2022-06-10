from writer.engine import model

def create_model_tree():
    # This is from "A STUDY IN SCARLET." by "A. Conan Doyle".
    # It is in public domain and can therefore easily be used for this purpose.

    print("Document: 'A Study in Scarlet'")

    model_tree = model.DocumentModelNode()

    heading_paragraph_style = model.ModelStyle(
        parent_model_style=model_tree.get_style(),
        is_bold=True,
        font_size=18.0,
    )
    normal_paragraph_style = model.ModelStyle(
        parent_model_style=model_tree.get_style(),
        font_size=12.0,
    )

    normal_heading_text_chunk_style = model.ModelStyle(
        parent_model_style=heading_paragraph_style,
    )
    normal_normal_text_chunk_style = model.ModelStyle(
        parent_model_style=normal_paragraph_style,
    )
    bold_normal_text_chunk_style = model.ModelStyle(
        parent_model_style=normal_paragraph_style,
        is_bold=True,
    )

    add_chapter_1(
        model_tree=model_tree,
        heading_paragraph_style=heading_paragraph_style,
        normal_paragraph_style=normal_paragraph_style,
        normal_heading_text_chunk_style=normal_heading_text_chunk_style,
        normal_normal_text_chunk_style=normal_normal_text_chunk_style,
        bold_normal_text_chunk_style=bold_normal_text_chunk_style,
    )

    add_chapter_2(
        model_tree=model_tree,
        heading_paragraph_style=heading_paragraph_style,
        normal_paragraph_style=normal_paragraph_style,
        normal_heading_text_chunk_style=normal_heading_text_chunk_style,
        normal_normal_text_chunk_style=normal_normal_text_chunk_style,
        bold_normal_text_chunk_style=bold_normal_text_chunk_style,
    )

    return model_tree

def add_chapter_1(*, model_tree, heading_paragraph_style, normal_paragraph_style, normal_heading_text_chunk_style, normal_normal_text_chunk_style, bold_normal_text_chunk_style):
    paragraph = model_tree.add_child(model.ParagraphModelNode(style=heading_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="CHAPTER I. MR. SHERLOCK HOLMES.", style=normal_heading_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="IN the year 1878 I took my degree of Doctor of Medicine of the University of London, and proceeded to Netley to go through the course prescribed for surgeons in the army. Having completed my studies there, I was duly attached to the Fifth Northumberland Fusiliers as Assistant Surgeon. The regiment was stationed in India at the time, and before I could join it, the second Afghan war had broken out. On landing at Bombay, I learned that my corps had advanced through the passes, and was already deep in the enemy’s country. I followed, however, with many other officers who were in the same situation as myself, and succeeded in reaching Candahar in safety, where I found my regiment, and at once entered upon my new duties.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="The campaign brought honours and promotion to many, but for me it had nothing but misfortune and disaster. I was removed from my brigade and attached to the Berkshires, with whom I served at the fatal battle of Maiwand. There I was struck on the shoulder by a Jezail bullet, which shattered the bone and grazed the subclavian artery. I should have fallen into the hands of the murderous Ghazis had it not been for the devotion and courage shown by Murray, my orderly, who threw me across a pack-horse, and succeeded in bringing me safely to the British lines.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Worn with pain, and weak from the prolonged hardships which I had undergone, I was removed, with a great train of wounded sufferers, to the base hospital at Peshawar. Here I rallied, and had already improved so far as to be able to walk about the wards, and even to bask a little upon the verandah, when I was struck down by enteric fever, that curse of our Indian possessions. For months my life was despaired of, and when at last I came to myself and became convalescent, I was so weak and emaciated that a medical board determined that not a day should be lost in sending me back to England. I was dispatched, accordingly, in the troopship “Orontes,” and landed a month later on Portsmouth jetty, with my health irretrievably ruined, but with permission from a paternal government to spend the next nine months in attempting to improve it.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I had neither kith nor kin in England, and was therefore as free as air—or as free as an income of eleven shillings and sixpence a day will permit a man to be. Under such circumstances, I naturally gravitated to London, that great cesspool into which all the loungers and idlers of the Empire are irresistibly drained. There I stayed for some time at a private hotel in the Strand, leading a comfortless, meaningless existence, and spending such money as I had, considerably more freely than I ought. So alarming did the state of my finances become, that I soon realized that I must either leave the metropolis and rusticate somewhere in the country, or that I must make a complete alteration in my style of living. Choosing the latter alternative, I began by making up my mind to leave the hotel, and to take up my quarters in some less pretentious and less expensive domicile.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="On the very day that I had come to this conclusion, I was standing at the Criterion Bar, when some one tapped me on the shoulder, and turning round I recognized young Stamford, who had been a dresser under me at Barts. The sight of a friendly face in the great wilderness of London is a pleasant thing indeed to a lonely man. In old days Stamford had never been a particular crony of mine, but now I hailed him with enthusiasm, and he, in his turn, appeared to be delighted to see me. In the exuberance of my joy, I asked him to lunch with me at the Holborn, and we started off together in a hansom.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Whatever have you been doing with yourself, Watson?” he asked in undisguised wonder, as we rattled through the crowded London streets. “You are as thin as a lath and as brown as a nut.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I gave him a short sketch of my adventures, and had hardly concluded it by the time that we reached our destination.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Poor devil!” he said, commiseratingly, after he had listened to my misfortunes. “What are you up to now?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Looking for lodgings.” 3 I answered. “Trying to solve the problem as to whether it is possible to get comfortable rooms at a reasonable price.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“That’s a strange thing,” remarked my companion; “you are the second man to-day that has used that expression to me.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“And who was the first?” I asked.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“A fellow who is working at the chemical laboratory up at the hospital. He was bemoaning himself this morning because he could not get someone to go halves with him in some nice rooms which he had found, and which were too much for his purse.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“By Jove!” I cried, “if he really wants someone to share the rooms and the expense, I am the very man for him. I should prefer having a partner to being alone.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Young Stamford looked rather strangely at me over his wine-glass. “You don’t know Sherlock Holmes yet,” he said; “perhaps you would not care for him as a constant companion.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Why, what is there against him?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Oh, I didn’t say there was anything against him. He is a little queer in his ideas—an enthusiast in some branches of science. As far as I know he is a decent fellow enough.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“A medical student, I suppose?” said I.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“No—I have no idea what he intends to go in for. I believe he is well up in anatomy, and he is a first-class chemist; but, as far as I know, he has never taken out any systematic medical classes. His studies are very desultory and eccentric, but he has amassed a lot of out-of-the way knowledge which would astonish his professors.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Did you never ask him what he was going in for?” I asked.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“No; he is not a man that it is easy to draw out, though he can be communicative enough when the fancy seizes him.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“I should like to meet him,” I said. “If I am to lodge with anyone, I should prefer a man of studious and quiet habits. I am not strong enough yet to stand much noise or excitement. I had enough of both in Afghanistan to last me for the remainder of my natural existence. How could I meet this friend of yours?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“He is sure to be at the laboratory,” returned my companion. “He either avoids the place for weeks, or else he works there from morning to night. If you like, we shall drive round together after luncheon.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Certainly,” I answered, and the conversation drifted away into other channels.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="As we made our way to the hospital after leaving the Holborn, Stamford gave me a few more particulars about the gentleman whom I proposed to take as a fellow-lodger.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You mustn’t blame me if you don’t get on with him,” he said; “I know nothing more of him than I have learned from meeting him occasionally in the laboratory. You proposed this arrangement, so you must not hold me responsible.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“If we don’t get on it will be easy to part company,” I answered. “It seems to me, Stamford,” I added, looking hard at my companion, “that you have some reason for washing your hands of the matter. Is this fellow’s temper so formidable, or what is it? Don’t be mealy-mouthed about it.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“It is not easy to express the inexpressible,” he answered with a laugh. “Holmes is a little too scientific for my tastes—it approaches to cold-bloodedness. I could imagine his giving a friend a little pinch of the latest vegetable alkaloid, not out of malevolence, you understand, but simply out of a spirit of inquiry in order to have an accurate idea of the effects. To do him justice, I think that he would take it himself with the same readiness. He appears to have a passion for definite and exact knowledge.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Very right too.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Yes, but it may be pushed to excess. When it comes to beating the subjects in the dissecting-rooms with a stick, it is certainly taking rather a bizarre shape.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Beating the subjects!”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Yes, to verify how far bruises may be produced after death. I saw him at it with my own eyes.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“And yet you say he is not a medical student?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“No. Heaven knows what the objects of his studies are. But here we are, and you must form your own impressions about him.” As he spoke, we turned down a narrow lane and passed through a small side-door, which opened into a wing of the great hospital. It was familiar ground to me, and I needed no guiding as we ascended the bleak stone staircase and made our way down the long corridor with its vista of whitewashed wall and dun-coloured doors. Near the further end a low arched passage branched away from it and led to the chemical laboratory.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="This was a lofty chamber, lined and littered with countless bottles. Broad, low tables were scattered about, which bristled with retorts, test-tubes, and little Bunsen lamps, with their blue flickering flames. There was only one student in the room, who was bending over a distant table absorbed in his work. At the sound of our steps he glanced round and sprang to his feet with a cry of pleasure. “I’ve found it! I’ve found it,” he shouted to my companion, running towards us with a test-tube in his hand. “I have found a re-agent which is precipitated by hoemoglobin, 4 and by nothing else.” Had he discovered a gold mine, greater delight could not have shone upon his features.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Dr. Watson, Mr. Sherlock Holmes,” said Stamford, introducing us.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“How are you?” he said cordially, gripping my hand with a strength for which I should hardly have given him credit. “You have been in Afghanistan, I perceive.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“How on earth did you know that?” I asked in astonishment.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Never mind,” said he, chuckling to himself. “The question now is about hoemoglobin. No doubt you see the significance of this discovery of mine?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“It is interesting, chemically, no doubt,” I answered, “but practically——”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Why, man, it is the most practical medico-legal discovery for years. Don’t you see that it gives us an infallible test for blood stains. Come over here now!” He seized me by the coat-sleeve in his eagerness, and drew me over to the table at which he had been working. “Let us have some fresh blood,” he said, digging a long bodkin into his finger, and drawing off the resulting drop of blood in a chemical pipette. “Now, I add this small quantity of blood to a litre of water. You perceive that the resulting mixture has the appearance of pure water. The proportion of blood cannot be more than one in a million. I have no doubt, however, that we shall be able to obtain the characteristic reaction.” As he spoke, he threw into the vessel a few white crystals, and then added some drops of a transparent fluid. In an instant the contents assumed a dull mahogany colour, and a brownish dust was precipitated to the bottom of the glass jar.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Ha! ha!” he cried, clapping his hands, and looking as delighted as a child with a new toy. “What do you think of that?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“It seems to be a very delicate test,” I remarked.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Beautiful! beautiful! The old Guiacum test was very clumsy and uncertain. So is the microscopic examination for blood corpuscles. The latter is valueless if the stains are a few hours old. Now, this appears to act as well whether the blood is old or new. Had this test been invented, there are hundreds of men now walking the earth who would long ago have paid the penalty of their crimes.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Indeed!” I murmured.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Criminal cases are continually hinging upon that one point. A man is suspected of a crime months perhaps after it has been committed. His linen or clothes are examined, and brownish stains discovered upon them. Are they blood stains, or mud stains, or rust stains, or fruit stains, or what are they? That is a question which has puzzled many an expert, and why? Because there was no reliable test. Now we have the Sherlock Holmes’ test, and there will no longer be any difficulty.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="His eyes fairly glittered as he spoke, and he put his hand over his heart and bowed as if to some applauding crowd conjured up by his imagination.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You are to be congratulated,” I remarked, considerably surprised at his enthusiasm.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“There was the case of Von Bischoff at Frankfort last year. He would certainly have been hung had this test been in existence. Then there was Mason of Bradford, and the notorious Muller, and Lefevre of Montpellier, and Samson of New Orleans. I could name a score of cases in which it would have been decisive.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You seem to be a walking calendar of crime,” said Stamford with a laugh. “You might start a paper on those lines. Call it the ‘Police News of the Past.’”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Very interesting reading it might be made, too,” remarked Sherlock Holmes, sticking a small piece of plaster over the prick on his finger. “I have to be careful,” he continued, turning to me with a smile, “for I dabble with poisons a good deal.” He held out his hand as he spoke, and I noticed that it was all mottled over with similar pieces of plaster, and discoloured with strong acids.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“We came here on business,” said Stamford, sitting down on a high three-legged stool, and pushing another one in my direction with his foot. “My friend here wants to take diggings, and as you were complaining that you could get no one to go halves with you, I thought that I had better bring you together.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Sherlock Holmes seemed delighted at the idea of sharing his rooms with me. “I have my eye on a suite in Baker Street,” he said, “which would suit us down to the ground. You don’t mind the smell of strong tobacco, I hope?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“I always smoke ‘ship’s’ myself,” I answered.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“That’s good enough. I generally have chemicals about, and occasionally do experiments. Would that annoy you?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“By no means.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Let me see—what are my other shortcomings. I get in the dumps at times, and don’t open my mouth for days on end. You must not think I am sulky when I do that. Just let me alone, and I’ll soon be right. What have you to confess now? It’s just as well for two fellows to know the worst of one another before they begin to live together.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I laughed at this cross-examination. “I keep a bull pup,” I said, “and I object to rows because my nerves are shaken, and I get up at all sorts of ungodly hours, and I am extremely lazy. I have another set of vices when I’m well, but those are the principal ones at present.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Do you include violin-playing in your category of rows?” he asked, anxiously.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“It depends on the player,” I answered. “A well-played violin is a treat for the gods—a badly-played one——”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Oh, that’s all right,” he cried, with a merry laugh. “I think we may consider the thing as settled—that is, if the rooms are agreeable to you.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“When shall we see them?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Call for me here at noon to-morrow, and we’ll go together and settle everything,” he answered.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“All right—noon exactly,” said I, shaking his hand.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="We left him working among his chemicals, and we walked together towards my hotel.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“By the way,” I asked suddenly, stopping and turning upon Stamford, “how the deuce did he know that I had come from Afghanistan?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="My companion smiled an enigmatical smile. “That’s just his little peculiarity,” he said. “A good many people have wanted to know how he finds things out.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Oh! a mystery is it?” I cried, rubbing my hands. “This is very piquant. I am much obliged to you for bringing us together. ‘The proper study of mankind is man,’ you know.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You must study him, then,” Stamford said, as he bade me good-bye. “You’ll find him a knotty problem, though. I’ll wager he learns more about you than you about him. Good-bye.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Good-bye,” I answered, and strolled on to my hotel, considerably interested in my new acquaintance.", style=normal_normal_text_chunk_style))

def add_chapter_2(*, model_tree, heading_paragraph_style, normal_paragraph_style, normal_heading_text_chunk_style, normal_normal_text_chunk_style, bold_normal_text_chunk_style):
    paragraph = model_tree.add_child(model.ParagraphModelNode(style=heading_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="CHAPTER II. THE SCIENCE OF DEDUCTION.", style=normal_heading_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="WE met next day as he had arranged, and inspected the rooms at No. 221B, 5 Baker Street, of which he had spoken at our meeting. They consisted of a couple of comfortable bed-rooms and a single large airy sitting-room, cheerfully furnished, and illuminated by two broad windows. So desirable in every way were the apartments, and so moderate did the terms seem when divided between us, that the bargain was concluded upon the spot, and we at once entered into possession. That very evening I moved my things round from the hotel, and on the following morning Sherlock Holmes followed me with several boxes and portmanteaus. For a day or two we were busily employed in unpacking and laying out our property to the best advantage. That done, we gradually began to settle down and to accommodate ourselves to our new surroundings.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Holmes was certainly not a difficult man to live with. He was quiet in his ways, and his habits were regular. It was rare for him to be up after ten at night, and he had invariably breakfasted and gone out before I rose in the morning. Sometimes he spent his day at the chemical laboratory, sometimes in the dissecting-rooms, and occasionally in long walks, which appeared to take him into the lowest portions of the City. Nothing could exceed his energy when the working fit was upon him; but now and again a reaction would seize him, and for days on end he would lie upon the sofa in the sitting-room, hardly uttering a word or moving a muscle from morning to night. On these occasions I have noticed such a dreamy, vacant expression in his eyes, that I might have suspected him of being addicted to the use of some narcotic, had not the temperance and cleanliness of his whole life forbidden such a notion.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="As the weeks went by, my interest in him and my curiosity as to his aims in life, gradually deepened and increased. His very person and appearance were such as to strike the attention of the most casual observer. In height he was rather over six feet, and so excessively lean that he seemed to be considerably taller. His eyes were sharp and piercing, save during those intervals of torpor to which I have alluded; and his thin, hawk-like nose gave his whole expression an air of alertness and decision. His chin, too, had the prominence and squareness which mark the man of determination. His hands were invariably blotted with ink and stained with chemicals, yet he was possessed of extraordinary delicacy of touch, as I frequently had occasion to observe when I watched him manipulating his fragile philosophical instruments.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="The reader may set me down as a hopeless busybody, when I confess how much this man stimulated my curiosity, and how often I endeavoured to break through the reticence which he showed on all that concerned himself. Before pronouncing judgment, however, be it remembered, how objectless was my life, and how little there was to engage my attention. My health forbade me from venturing out unless the weather was exceptionally genial, and I had no friends who would call upon me and break the monotony of my daily existence. Under these circumstances, I eagerly hailed the little mystery which hung around my companion, and spent much of my time in endeavouring to unravel it.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="He was not studying medicine. He had himself, in reply to a question, confirmed Stamford’s opinion upon that point. Neither did he appear to have pursued any course of reading which might fit him for a degree in science or any other recognized portal which would give him an entrance into the learned world. Yet his zeal for certain studies was remarkable, and within eccentric limits his knowledge was so extraordinarily ample and minute that his observations have fairly astounded me. Surely no man would work so hard or attain such precise information unless he had some definite end in view. Desultory readers are seldom remarkable for the exactness of their learning. No man burdens his mind with small matters unless he has some very good reason for doing so.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="His ignorance was as remarkable as his knowledge. Of contemporary literature, philosophy and politics he appeared to know next to nothing. Upon my quoting Thomas Carlyle, he inquired in the naivest way who he might be and what he had done. My surprise reached a climax, however, when I found incidentally that he was ignorant of the Copernican Theory and of the composition of the Solar System. That any civilized human being in this nineteenth century should not be aware that the earth travelled round the sun appeared to be to me such an extraordinary fact that I could hardly realize it.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You appear to be astonished,” he said, smiling at my expression of surprise. “Now that I do know it I shall do my best to forget it.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“To forget it!”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You see,” he explained, “I consider that a man’s brain originally is like a little empty attic, and you have to stock it with such furniture as you choose. A fool takes in all the lumber of every sort that he comes across, so that the knowledge which might be useful to him gets crowded out, or at best is jumbled up with a lot of other things so that he has a difficulty in laying his hands upon it. Now the skilful workman is very careful indeed as to what he takes into his brain-attic. He will have nothing but the tools which may help him in doing his work, but of these he has a large assortment, and all in the most perfect order. It is a mistake to think that that little room has elastic walls and can distend to any extent. Depend upon it there comes a time when for every addition of knowledge you forget something that you knew before. It is of the highest importance, therefore, not to have useless facts elbowing out the useful ones.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“But the Solar System!” I protested.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“What the deuce is it to me?” he interrupted impatiently; “you say that we go round the sun. If we went round the moon it would not make a pennyworth of difference to me or to my work.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I was on the point of asking him what that work might be, but something in his manner showed me that the question would be an unwelcome one. I pondered over our short conversation, however, and endeavoured to draw my deductions from it. He said that he would acquire no knowledge which did not bear upon his object. Therefore all the knowledge which he possessed was such as would be useful to him. I enumerated in my own mind all the various points upon which he had shown me that he was exceptionally well-informed. I even took a pencil and jotted them down. I could not help smiling at the document when I had completed it. It ran in this way—", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="SHERLOCK HOLMES—his limits.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  1. Knowledge of Literature.—Nil.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  2.              Philosophy.—Nil.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  3.              Astronomy.—Nil.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  4.              Politics.—Feeble.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  5.              Botany.—Variable.  Well up in belladonna,", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                              opium, and poisons generally.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                              Knows nothing of practical gardening.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  6.              Geology.—Practical, but limited.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               Tells at a glance different soils", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               from each other.  After walks has", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               shown me splashes upon his trousers,", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               and told me by their colour and", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               consistence in what part of London", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                               he had received them.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  7.              Chemistry.—Profound.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  8.              Anatomy.—Accurate, but unsystematic.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  9.              Sensational Literature.—Immense.  He appears", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                              to know every detail of every horror", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="                              perpetrated in the century.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  10. Plays the violin well.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  11. Is an expert singlestick player, boxer, and swordsman.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="  12. Has a good practical knowledge of British law.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="When I had got so far in my list I threw it into the fire in despair. “If I can only find what the fellow is driving at by reconciling all these accomplishments, and discovering a calling which needs them all,” I said to myself, “I may as well give up the attempt at once.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I see that I have alluded above to his powers upon the violin. These were very remarkable, but as eccentric as all his other accomplishments. That he could play pieces, and difficult pieces, I knew well, because at my request he has played me some of Mendelssohn’s Lieder, and other favourites. When left to himself, however, he would seldom produce any music or attempt any recognized air. Leaning back in his arm-chair of an evening, he would close his eyes and scrape carelessly at the fiddle which was thrown across his knee. Sometimes the chords were sonorous and melancholy. Occasionally they were fantastic and cheerful. Clearly they reflected the thoughts which possessed him, but whether the music aided those thoughts, or whether the playing was simply the result of a whim or fancy was more than I could determine. I might have rebelled against these exasperating solos had it not been that he usually terminated them by playing in quick succession a whole series of my favourite airs as a slight compensation for the trial upon my patience.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="During the first week or so we had no callers, and I had begun to think that my companion was as friendless a man as I was myself. Presently, however, I found that he had many acquaintances, and those in the most different classes of society. There was one little sallow rat-faced, dark-eyed fellow who was introduced to me as Mr. Lestrade, and who came three or four times in a single week. One morning a young girl called, fashionably dressed, and stayed for half an hour or more. The same afternoon brought a grey-headed, seedy visitor, looking like a Jew pedlar, who appeared to me to be much excited, and who was closely followed by a slip-shod elderly woman. On another occasion an old white-haired gentleman had an interview with my companion; and on another a railway porter in his velveteen uniform. When any of these nondescript individuals put in an appearance, Sherlock Holmes used to beg for the use of the sitting-room, and I would retire to my bed-room. He always apologized to me for putting me to this inconvenience. “I have to use this room as a place of business,” he said, “and these people are my clients.” Again I had an opportunity of asking him a point blank question, and again my delicacy prevented me from forcing another man to confide in me. I imagined at the time that he had some strong reason for not alluding to it, but he soon dispelled the idea by coming round to the subject of his own accord.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="It was upon the 4th of March, as I have good reason to remember, that I rose somewhat earlier than usual, and found that Sherlock Holmes had not yet finished his breakfast. The landlady had become so accustomed to my late habits that my place had not been laid nor my coffee prepared. With the unreasonable petulance of mankind I rang the bell and gave a curt intimation that I was ready. Then I picked up a magazine from the table and attempted to while away the time with it, while my companion munched silently at his toast. One of the articles had a pencil mark at the heading, and I naturally began to run my eye through it.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Its somewhat ambitious title was “The Book of Life,” and it attempted to show how much an observant man might learn by an accurate and systematic examination of all that came in his way. It struck me as being a remarkable mixture of shrewdness and of absurdity. The reasoning was close and intense, but the deductions appeared to me to be far-fetched and exaggerated. The writer claimed by a momentary expression, a twitch of a muscle or a glance of an eye, to fathom a man’s inmost thoughts. Deceit, according to him, was an impossibility in the case of one trained to observation and analysis. His conclusions were as infallible as so many propositions of Euclid. So startling would his results appear to the uninitiated that until they learned the processes by which he had arrived at them they might well consider him as a necromancer.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“From a drop of water,” said the writer, “a logician could infer the possibility of an Atlantic or a Niagara without having seen or heard of one or the other. So all life is a great chain, the nature of which is known whenever we are shown a single link of it. Like all other arts, the Science of Deduction and Analysis is one which can only be acquired by long and patient study nor is life long enough to allow any mortal to attain the highest possible perfection in it. Before turning to those moral and mental aspects of the matter which present the greatest difficulties, let the enquirer begin by mastering more elementary problems. Let him, on meeting a fellow-mortal, learn at a glance to distinguish the history of the man, and the trade or profession to which he belongs. Puerile as such an exercise may seem, it sharpens the faculties of observation, and teaches one where to look and what to look for. By a man’s finger nails, by his coat-sleeve, by his boot, by his trouser knees, by the callosities of his forefinger and thumb, by his expression, by his shirt cuffs—by each of these things a man’s calling is plainly revealed. That all united should fail to enlighten the competent enquirer in any case is almost inconceivable.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“What ineffable twaddle!” I cried, slapping the magazine down on the table, “I never read such rubbish in my life.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“What is it?” asked Sherlock Holmes.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Why, this article,” I said, pointing at it with my egg spoon as I sat down to my breakfast. “I see that you have read it since you have marked it. I don’t deny that it is smartly written. It irritates me though. It is evidently the theory of some arm-chair lounger who evolves all these neat little paradoxes in the seclusion of his own study. It is not practical. I should like to see him clapped down in a third class carriage on the Underground, and asked to give the trades of all his fellow-travellers. I would lay a thousand to one against him.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You would lose your money,” Sherlock Holmes remarked calmly. “As for the article I wrote it myself.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You!”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Yes, I have a turn both for observation and for deduction. The theories which I have expressed there, and which appear to you to be so chimerical are really extremely practical—so practical that I depend upon them for my bread and cheese.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“And how?” I asked involuntarily.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Well, I have a trade of my own. I suppose I am the only one in the world. I’m a consulting detective, if you can understand what that is. Here in London we have lots of Government detectives and lots of private ones. When these fellows are at fault they come to me, and I manage to put them on the right scent. They lay all the evidence before me, and I am generally able, by the help of my knowledge of the history of crime, to set them straight. There is a strong family resemblance about misdeeds, and if you have all the details of a thousand at your finger ends, it is odd if you can’t unravel the thousand and first. Lestrade is a well-known detective. He got himself into a fog recently over a forgery case, and that was what brought him here.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“And these other people?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“They are mostly sent on by private inquiry agencies. They are all people who are in trouble about something, and want a little enlightening. I listen to their story, they listen to my comments, and then I pocket my fee.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“But do you mean to say,” I said, “that without leaving your room you can unravel some knot which other men can make nothing of, although they have seen every detail for themselves?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Quite so. I have a kind of intuition that way. Now and again a case turns up which is a little more complex. Then I have to bustle about and see things with my own eyes. You see I have a lot of special knowledge which I apply to the problem, and which facilitates matters wonderfully. Those rules of deduction laid down in that article which aroused your scorn, are invaluable to me in practical work. Observation with me is second nature. You appeared to be surprised when I told you, on our first meeting, that you had come from Afghanistan.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You were told, no doubt.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Nothing of the sort. I knew you came from Afghanistan. From long habit the train of thoughts ran so swiftly through my mind, that I arrived at the conclusion without being conscious of intermediate steps. There were such steps, however. The train of reasoning ran, ‘Here is a gentleman of a medical type, but with the air of a military man. Clearly an army doctor, then. He has just come from the tropics, for his face is dark, and that is not the natural tint of his skin, for his wrists are fair. He has undergone hardship and sickness, as his haggard face says clearly. His left arm has been injured. He holds it in a stiff and unnatural manner. Where in the tropics could an English army doctor have seen much hardship and got his arm wounded? Clearly in Afghanistan.’ The whole train of thought did not occupy a second. I then remarked that you came from Afghanistan, and you were astonished.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“It is simple enough as you explain it,” I said, smiling. “You remind me of Edgar Allen Poe’s Dupin. I had no idea that such individuals did exist outside of stories.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Sherlock Holmes rose and lit his pipe. “No doubt you think that you are complimenting me in comparing me to Dupin,” he observed. “Now, in my opinion, Dupin was a very inferior fellow. That trick of his of breaking in on his friends’ thoughts with an apropos remark after a quarter of an hour’s silence is really very showy and superficial. He had some analytical genius, no doubt; but he was by no means such a phenomenon as Poe appeared to imagine.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Have you read Gaboriau’s works?” I asked. “Does Lecoq come up to your idea of a detective?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Sherlock Holmes sniffed sardonically. “Lecoq was a miserable bungler,” he said, in an angry voice; “he had only one thing to recommend him, and that was his energy. That book made me positively ill. The question was how to identify an unknown prisoner. I could have done it in twenty-four hours. Lecoq took six months or so. It might be made a text-book for detectives to teach them what to avoid.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I felt rather indignant at having two characters whom I had admired treated in this cavalier style. I walked over to the window, and stood looking out into the busy street. “This fellow may be very clever,” I said to myself, “but he is certainly very conceited.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“There are no crimes and no criminals in these days,” he said, querulously. “What is the use of having brains in our profession. I know well that I have it in me to make my name famous. No man lives or has ever lived who has brought the same amount of study and of natural talent to the detection of crime which I have done. And what is the result? There is no crime to detect, or, at most, some bungling villainy with a motive so transparent that even a Scotland Yard official can see through it.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="I was still annoyed at his bumptious style of conversation. I thought it best to change the topic.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“I wonder what that fellow is looking for?” I asked, pointing to a stalwart, plainly-dressed individual who was walking slowly down the other side of the street, looking anxiously at the numbers. He had a large blue envelope in his hand, and was evidently the bearer of a message.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“You mean the retired sergeant of Marines,” said Sherlock Holmes.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Brag and bounce!” thought I to myself. “He knows that I cannot verify his guess.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="The thought had hardly passed through my mind when the man whom we were watching caught sight of the number on our door, and ran rapidly across the roadway. We heard a loud knock, a deep voice below, and heavy steps ascending the stair.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“For Mr. Sherlock Holmes,” he said, stepping into the room and handing my friend the letter.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="Here was an opportunity of taking the conceit out of him. He little thought of this when he made that random shot. “May I ask, my lad,” I said, in the blandest voice, “what your trade may be?”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“Commissionaire, sir,” he said, gruffly. “Uniform away for repairs.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“And you were?” I asked, with a slightly malicious glance at my companion.", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="“A sergeant, sir, Royal Marine Light Infantry, sir. No answer? Right, sir.”", style=normal_normal_text_chunk_style))

    paragraph = model_tree.add_child(model.ParagraphModelNode(style=normal_paragraph_style))
    paragraph.add_child(model.TextChunkModelNode(text="He clicked his heels together, raised his hand in a salute, and was gone.", style=normal_normal_text_chunk_style))

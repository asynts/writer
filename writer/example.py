import writer.engine.model as model
import writer.engine.tree as tree

default_style = model.ModelStyle()

normal_paragraph_style = model.ModelStyle(
    font_size=12.0,
    is_bold=False,
    is_italic=False,
)

heading_paragraph_style = model.ModelStyle(
    font_size=18.0,
    is_bold=True,
    is_italic=False,
)

normal_text_chunk_style = model.ModelStyle()

bold_text_chunk_style = model.ModelStyle(
    is_bold=True,
)

def create_model_tree(*, b_print_document_name: bool = True):
    return create_model_tree_small_document(b_print_document_name=b_print_document_name)

def create_model_tree_small_document(*, b_print_document_name: bool):
    if b_print_document_name:
        print("Document: 'Small Document'")

    model_tree = model.DocumentModelNode(
        style=default_style,
        children=[],
    )

    paragraph = model.ParagraphModelNode(
        style=heading_paragraph_style,
        children=[],
    )

    text_chunk = model.TextChunkModelNode(
        style=normal_text_chunk_style,
        text="Title",
        children=[],
    )
    text_chunk.make_immutable()
    paragraph.append_child(text_chunk)

    paragraph.make_immutable()
    model_tree.append_child(paragraph)

    paragraph = model.ParagraphModelNode(
        style=normal_paragraph_style,
        children=[],
    )

    text_chunk = model.TextChunkModelNode(
        style=normal_text_chunk_style,
        text="This is a paragraph. ",
        children=[],
    )
    text_chunk.make_immutable()
    paragraph.append_child(text_chunk)

    text_chunk = model.TextChunkModelNode(
        style=bold_text_chunk_style,
        text=" This is bold!",
        children=[],
    )
    text_chunk.make_immutable()
    paragraph.append_child(text_chunk)

    paragraph.make_immutable()
    model_tree.append_child(paragraph)

    model_tree.make_immutable()

    return model_tree

def create_paragraph_subtree(
    *,
    text: str,
    paragraph_style: model.ModelStyle = normal_paragraph_style,
    text_chunk_style: model.ModelStyle = normal_text_chunk_style,
):
    paragraph = model.ParagraphModelNode(
        style=paragraph_style,
        children=[],
    )

    text_chunk = model.TextChunkModelNode(
        style=text_chunk_style,
        text=text,
        children=[],
    )
    text_chunk.make_immutable()

    paragraph.append_child(text_chunk)
    paragraph.make_immutable()

    return paragraph

def create_model_tree_study(*, b_print_document_name: bool):
    # This is generated from 'Meta/study-in-scarlet.txt'.
    # Obviously, that text wasn't written by me, but it's in public domain.
    #
    # awk '{ if (NF > 0) { printf "    model_tree.append_child(create_paragraph_subtree(\n        text=\"%s\",\n    ))\n", $0 } }' Meta/study-in-scarlet.txt

    # This is from "A STUDY IN SCARLET." by "A. Conan Doyle".
    # It is in public domain and can therefore easily be used for this purpose.

    if b_print_document_name:
        print("Document: 'A Study in Scarlet'")

    model_tree = model.DocumentModelNode(
        style=default_style,
        children=[],
    )

    model_tree.append_child(create_paragraph_subtree(
        text="CHAPTER I. MR. SHERLOCK HOLMES.",
        paragraph_style=heading_paragraph_style,
        text_chunk_style=normal_text_chunk_style,
    ))

    model_tree.append_child(create_paragraph_subtree(
        text="IN the year 1878 I took my degree of Doctor of Medicine of the University of London, and proceeded to Netley to go through the course prescribed for surgeons in the army. Having completed my studies there, I was duly attached to the Fifth Northumberland Fusiliers as Assistant Surgeon. The regiment was stationed in India at the time, and before I could join it, the second Afghan war had broken out. On landing at Bombay, I learned that my corps had advanced through the passes, and was already deep in the enemy’s country. I followed, however, with many other officers who were in the same situation as myself, and succeeded in reaching Candahar in safety, where I found my regiment, and at once entered upon my new duties.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="The campaign brought honours and promotion to many, but for me it had nothing but misfortune and disaster. I was removed from my brigade and attached to the Berkshires, with whom I served at the fatal battle of Maiwand. There I was struck on the shoulder by a Jezail bullet, which shattered the bone and grazed the subclavian artery. I should have fallen into the hands of the murderous Ghazis had it not been for the devotion and courage shown by Murray, my orderly, who threw me across a pack-horse, and succeeded in bringing me safely to the British lines.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="Worn with pain, and weak from the prolonged hardships which I had undergone, I was removed, with a great train of wounded sufferers, to the base hospital at Peshawar. Here I rallied, and had already improved so far as to be able to walk about the wards, and even to bask a little upon the verandah, when I was struck down by enteric fever, that curse of our Indian possessions. For months my life was despaired of, and when at last I came to myself and became convalescent, I was so weak and emaciated that a medical board determined that not a day should be lost in sending me back to England. I was dispatched, accordingly, in the troopship “Orontes,” and landed a month later on Portsmouth jetty, with my health irretrievably ruined, but with permission from a paternal government to spend the next nine months in attempting to improve it.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="I had neither kith nor kin in England, and was therefore as free as air—or as free as an income of eleven shillings and sixpence a day will permit a man to be. Under such circumstances, I naturally gravitated to London, that great cesspool into which all the loungers and idlers of the Empire are irresistibly drained. There I stayed for some time at a private hotel in the Strand, leading a comfortless, meaningless existence, and spending such money as I had, considerably more freely than I ought. So alarming did the state of my finances become, that I soon realized that I must either leave the metropolis and rusticate somewhere in the country, or that I must make a complete alteration in my style of living. Choosing the latter alternative, I began by making up my mind to leave the hotel, and to take up my quarters in some less pretentious and less expensive domicile.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="On the very day that I had come to this conclusion, I was standing at the Criterion Bar, when some one tapped me on the shoulder, and turning round I recognized young Stamford, who had been a dresser under me at Barts. The sight of a friendly face in the great wilderness of London is a pleasant thing indeed to a lonely man. In old days Stamford had never been a particular crony of mine, but now I hailed him with enthusiasm, and he, in his turn, appeared to be delighted to see me. In the exuberance of my joy, I asked him to lunch with me at the Holborn, and we started off together in a hansom.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Whatever have you been doing with yourself, Watson?” he asked in undisguised wonder, as we rattled through the crowded London streets. “You are as thin as a lath and as brown as a nut.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="I gave him a short sketch of my adventures, and had hardly concluded it by the time that we reached our destination.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Poor devil!” he said, commiseratingly, after he had listened to my misfortunes. “What are you up to now?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Looking for lodgings.” 3 I answered. “Trying to solve the problem as to whether it is possible to get comfortable rooms at a reasonable price.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“That’s a strange thing,” remarked my companion; “you are the second man to-day that has used that expression to me.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“And who was the first?” I asked.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“A fellow who is working at the chemical laboratory up at the hospital. He was bemoaning himself this morning because he could not get someone to go halves with him in some nice rooms which he had found, and which were too much for his purse.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“By Jove!” I cried, “if he really wants someone to share the rooms and the expense, I am the very man for him. I should prefer having a partner to being alone.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="Young Stamford looked rather strangely at me over his wine-glass. “You don’t know Sherlock Holmes yet,” he said; “perhaps you would not care for him as a constant companion.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Why, what is there against him?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Oh, I didn’t say there was anything against him. He is a little queer in his ideas—an enthusiast in some branches of science. As far as I know he is a decent fellow enough.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“A medical student, I suppose?” said I.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“No—I have no idea what he intends to go in for. I believe he is well up in anatomy, and he is a first-class chemist; but, as far as I know, he has never taken out any systematic medical classes. His studies are very desultory and eccentric, but he has amassed a lot of out-of-the way knowledge which would astonish his professors.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Did you never ask him what he was going in for?” I asked.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“No; he is not a man that it is easy to draw out, though he can be communicative enough when the fancy seizes him.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“I should like to meet him,” I said. “If I am to lodge with anyone, I should prefer a man of studious and quiet habits. I am not strong enough yet to stand much noise or excitement. I had enough of both in Afghanistan to last me for the remainder of my natural existence. How could I meet this friend of yours?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“He is sure to be at the laboratory,” returned my companion. “He either avoids the place for weeks, or else he works there from morning to night. If you like, we shall drive round together after luncheon.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Certainly,” I answered, and the conversation drifted away into other channels.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="As we made our way to the hospital after leaving the Holborn, Stamford gave me a few more particulars about the gentleman whom I proposed to take as a fellow-lodger.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“You mustn’t blame me if you don’t get on with him,” he said; “I know nothing more of him than I have learned from meeting him occasionally in the laboratory. You proposed this arrangement, so you must not hold me responsible.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“If we don’t get on it will be easy to part company,” I answered. “It seems to me, Stamford,” I added, looking hard at my companion, “that you have some reason for washing your hands of the matter. Is this fellow’s temper so formidable, or what is it? Don’t be mealy-mouthed about it.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“It is not easy to express the inexpressible,” he answered with a laugh. “Holmes is a little too scientific for my tastes—it approaches to cold-bloodedness. I could imagine his giving a friend a little pinch of the latest vegetable alkaloid, not out of malevolence, you understand, but simply out of a spirit of inquiry in order to have an accurate idea of the effects. To do him justice, I think that he would take it himself with the same readiness. He appears to have a passion for definite and exact knowledge.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Very right too.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Yes, but it may be pushed to excess. When it comes to beating the subjects in the dissecting-rooms with a stick, it is certainly taking rather a bizarre shape.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Beating the subjects!”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Yes, to verify how far bruises may be produced after death. I saw him at it with my own eyes.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“And yet you say he is not a medical student?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“No. Heaven knows what the objects of his studies are. But here we are, and you must form your own impressions about him.” As he spoke, we turned down a narrow lane and passed through a small side-door, which opened into a wing of the great hospital. It was familiar ground to me, and I needed no guiding as we ascended the bleak stone staircase and made our way down the long corridor with its vista of whitewashed wall and dun-coloured doors. Near the further end a low arched passage branched away from it and led to the chemical laboratory.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="This was a lofty chamber, lined and littered with countless bottles. Broad, low tables were scattered about, which bristled with retorts, test-tubes, and little Bunsen lamps, with their blue flickering flames. There was only one student in the room, who was bending over a distant table absorbed in his work. At the sound of our steps he glanced round and sprang to his feet with a cry of pleasure. “I’ve found it! I’ve found it,” he shouted to my companion, running towards us with a test-tube in his hand. “I have found a re-agent which is precipitated by hoemoglobin, 4 and by nothing else.” Had he discovered a gold mine, greater delight could not have shone upon his features.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Dr. Watson, Mr. Sherlock Holmes,” said Stamford, introducing us.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“How are you?” he said cordially, gripping my hand with a strength for which I should hardly have given him credit. “You have been in Afghanistan, I perceive.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“How on earth did you know that?” I asked in astonishment.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Never mind,” said he, chuckling to himself. “The question now is about hoemoglobin. No doubt you see the significance of this discovery of mine?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“It is interesting, chemically, no doubt,” I answered, “but practically——”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Why, man, it is the most practical medico-legal discovery for years. Don’t you see that it gives us an infallible test for blood stains. Come over here now!” He seized me by the coat-sleeve in his eagerness, and drew me over to the table at which he had been working. “Let us have some fresh blood,” he said, digging a long bodkin into his finger, and drawing off the resulting drop of blood in a chemical pipette. “Now, I add this small quantity of blood to a litre of water. You perceive that the resulting mixture has the appearance of pure water. The proportion of blood cannot be more than one in a million. I have no doubt, however, that we shall be able to obtain the characteristic reaction.” As he spoke, he threw into the vessel a few white crystals, and then added some drops of a transparent fluid. In an instant the contents assumed a dull mahogany colour, and a brownish dust was precipitated to the bottom of the glass jar.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Ha! ha!” he cried, clapping his hands, and looking as delighted as a child with a new toy. “What do you think of that?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“It seems to be a very delicate test,” I remarked.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Beautiful! beautiful! The old Guiacum test was very clumsy and uncertain. So is the microscopic examination for blood corpuscles. The latter is valueless if the stains are a few hours old. Now, this appears to act as well whether the blood is old or new. Had this test been invented, there are hundreds of men now walking the earth who would long ago have paid the penalty of their crimes.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Indeed!” I murmured.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Criminal cases are continually hinging upon that one point. A man is suspected of a crime months perhaps after it has been committed. His linen or clothes are examined, and brownish stains discovered upon them. Are they blood stains, or mud stains, or rust stains, or fruit stains, or what are they? That is a question which has puzzled many an expert, and why? Because there was no reliable test. Now we have the Sherlock Holmes’ test, and there will no longer be any difficulty.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="His eyes fairly glittered as he spoke, and he put his hand over his heart and bowed as if to some applauding crowd conjured up by his imagination.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“You are to be congratulated,” I remarked, considerably surprised at his enthusiasm.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“There was the case of Von Bischoff at Frankfort last year. He would certainly have been hung had this test been in existence. Then there was Mason of Bradford, and the notorious Muller, and Lefevre of Montpellier, and Samson of New Orleans. I could name a score of cases in which it would have been decisive.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“You seem to be a walking calendar of crime,” said Stamford with a laugh. “You might start a paper on those lines. Call it the ‘Police News of the Past.’”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Very interesting reading it might be made, too,” remarked Sherlock Holmes, sticking a small piece of plaster over the prick on his finger. “I have to be careful,” he continued, turning to me with a smile, “for I dabble with poisons a good deal.” He held out his hand as he spoke, and I noticed that it was all mottled over with similar pieces of plaster, and discoloured with strong acids.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“We came here on business,” said Stamford, sitting down on a high three-legged stool, and pushing another one in my direction with his foot. “My friend here wants to take diggings, and as you were complaining that you could get no one to go halves with you, I thought that I had better bring you together.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="Sherlock Holmes seemed delighted at the idea of sharing his rooms with me. “I have my eye on a suite in Baker Street,” he said, “which would suit us down to the ground. You don’t mind the smell of strong tobacco, I hope?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“I always smoke ‘ship’s’ myself,” I answered.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“That’s good enough. I generally have chemicals about, and occasionally do experiments. Would that annoy you?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“By no means.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Let me see—what are my other shortcomings. I get in the dumps at times, and don’t open my mouth for days on end. You must not think I am sulky when I do that. Just let me alone, and I’ll soon be right. What have you to confess now? It’s just as well for two fellows to know the worst of one another before they begin to live together.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="I laughed at this cross-examination. “I keep a bull pup,” I said, “and I object to rows because my nerves are shaken, and I get up at all sorts of ungodly hours, and I am extremely lazy. I have another set of vices when I’m well, but those are the principal ones at present.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Do you include violin-playing in your category of rows?” he asked, anxiously.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“It depends on the player,” I answered. “A well-played violin is a treat for the gods—a badly-played one——”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Oh, that’s all right,” he cried, with a merry laugh. “I think we may consider the thing as settled—that is, if the rooms are agreeable to you.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“When shall we see them?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Call for me here at noon to-morrow, and we’ll go together and settle everything,” he answered.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“All right—noon exactly,” said I, shaking his hand.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="We left him working among his chemicals, and we walked together towards my hotel.",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“By the way,” I asked suddenly, stopping and turning upon Stamford, “how the deuce did he know that I had come from Afghanistan?”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="My companion smiled an enigmatical smile. “That’s just his little peculiarity,” he said. “A good many people have wanted to know how he finds things out.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Oh! a mystery is it?” I cried, rubbing my hands. “This is very piquant. I am much obliged to you for bringing us together. ‘The proper study of mankind is man,’ you know.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“You must study him, then,” Stamford said, as he bade me good-bye. “You’ll find him a knotty problem, though. I’ll wager he learns more about you than you about him. Good-bye.”",
    ))
    model_tree.append_child(create_paragraph_subtree(
        text="“Good-bye,” I answered, and strolled on to my hotel, considerably interested in my new acquaintance.",
    ))

    model_tree.make_immutable()
    return model_tree

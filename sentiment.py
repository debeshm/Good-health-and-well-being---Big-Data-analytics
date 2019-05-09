from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

sia = SIA()
results = []

headlines=["I am suffering from fever", "I am having a headache", "kill those bastards", "I want to strike an airplane to new WTC", "music fever", "My kid is suffering from fever", "meseals is growing fast", "सर दबग लोगों से मेरे जानमाल की सुरक्षा करा । इन दबग लोगो के सामने आज शास्त्री पार्क थाने कि पुलिस भी बेबस…", "I’m going to kill myself ... mariachi band playing in the restaurant when I have a headache", "I had a headache today so I couldn’t go anywhere and do much. I laced in bed 75% of the time.", "Wake up with a sinus headache aaand the guy across the street cutting the grass (from before 7)... Let's restart this day eh?"]

for line in headlines:
    pol_score = sia.polarity_scores(line)
    pol_score['headline'] = line
    results.append(pol_score)

for i in results:
    print(i)
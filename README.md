# RU-Okay-
https://devpost.com/software/ru-okay
##Inspiration
Healthcare costs are on the rise - drugs are being promoted on national media, some doctors partner with companies to get commission in return for higher prescriptions rates. Many drugs have similar purposes, but vastly different side effects and costs, leaving patients wondering why their doctor prescribed a specific medicine over a cheaper or less adverse one. RU Okay? is here to fix that.

##What it does
RU Okay? gives the power of medicinal data back to the patients.

##How we built it
Medicinal data is notoriously fragmented and unregulated. Once the infection is inputted, it is searched in the NIH (National Institutes of Health) RxNav database for its NUI code. This database is used again to provide drugs (active ingredients) that could cure the infection, and their respective NUI codes. For each of these ingredients, another NIH database is queried to find brands that sell a drug containing this active ingredient. Each active ingredient is then looked up in the NIH NDF-RT dataset to find the RXCUI code, another identifier.

To find the side effects of each drug and their occurence rates, we look at the FDA's (Food and Drug Administration) Drug Adverse Events dataset, which is queried using the RXCUI code. The results are manipulated using Python Pandas to find the percentage occurrence of each side effect.

Finally, the Medicaid NADAC (National Average Drug Acquisition Cost) dataset is used to find the distributions of each drug, and its average cost of acquisition. This entire script is hosted on a server using Flask and ngrok, and made into the RESTful API, which takes in the type of disease and returns a JSON of all the data described.

The iOS app provides a basic interface for our dataset that can interact with the server. It displays the side effects and their occurrence percentages for each active ingredient by parsing the JSON. This is out example usecase.

The python script increases functionality to be able to sort drugs by cost, and provides graphics that let patients have a better idea of what they are being prescribed.

##What's next for RU Okay?
By giving patients and doctors access to more drug data, we hope to push costs down for drugs and improve overall healthcare. Patients should be able to select drugs that are covered by their insurance plan, and minimize side effects they don't want. Doctors should be able to give their patients a better understanding of what they are prescribing.

The answer to RU Okay? should always by a resounding YES.

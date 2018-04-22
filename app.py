from flask import Flask, request
import json
import requests
import pandas as pd
import math
import numpy as np
app = Flask(__name__)


@app.route("/disease")
def diseaseR():
    dname = request.args.get('name')
    return get_json(dname);
    
    
def get_json(infection):
    # GET THE NUID for the INFECTION
    infection = infection.replace(" ", "%20")
    response = requests.get('https://rxnav.nlm.nih.gov/REST/Ndfrt/search.json?conceptName='+infection+'&kindName=DISEASE_KIND')
    d = response.json()
    if (d['groupConcepts'][0] == None):
        print("ERROR! Infection not found!")
        return "ERROR! INFECTION NOT FOUND!"
        
    else:    
        nui = d['groupConcepts'][0]['concept'][0]['conceptNui']

    # GET INGREDIENTS THAT CAN FIX THE GIVEN INFECTION
    response2 = requests.get('https://rxnav.nlm.nih.gov/REST/Ndfrt/reverse.json?nui='+nui+'&roleName=may_treat%20{NDFRT}&transitive=false')
    ingredients = response2.json()
    ing_list = ingredients['groupConcepts'][0]['concept']    

    # MAKE THE NAMES AND NUIDS OF ALL THE FIXES
    nuis = []
    names = []
    for x in ing_list:
        names.append(x['conceptName'])
        nuis.append(x['conceptNui'])
        
    # CONSTRUCT THE OUTPUT DICTIONARY
    outdict = {}
    for i in range(len(names)):
        outdict[names[i]] = {
            'nui': nuis[i],
            'rxcui': 0,
            'sideeffects': {},
            'brands': []
        }
        
        
    # GET ANOTHER ID FOR THE DRUGS, delete the ones that don't have an ID
    rxid = []
    for s in names:
        f = (requests.get('https://rxnav.nlm.nih.gov/REST/rxcui.json?name='+s))
        f = f.json()
        try:
            rxid.append(f['idGroup']['rxnormId'][0])
            outdict[s]['rxcui'] = f['idGroup']['rxnormId'][0]
        except:
            del outdict[s]
            continue

    for key in outdict:
        b = requests.get('https://rxnav.nlm.nih.gov/REST/brands.json?ingredientids='+outdict[key]['rxcui'])
        x = b.json()
        x = x['brandGroup']
        if 'conceptProperties' in x.keys():
            x = x['conceptProperties']
            for y in x:
                outdict[key]['brands'].append(y['name'])


    bad = []

    for key in outdict:
        q = requests.get('https://api.fda.gov/drug/event.json?search=patient.drug.openfda.substance_name:"'+key+'"&count=patient.reaction.reactionmeddrapt.exact')
        if 'error' in q.json():
            bad.append(key)
            continue
        df = pd.DataFrame(q.json()['results'])
        total = df['count'].sum()
        df['percentage'] = (df['count']*100//total).astype(int)
        
        for i in range(min(10, len(df))):
            outdict[key]['sideeffects'][df.iloc[i]['term']] = np.asscalar(df.iloc[i]['percentage'])

    for b in bad:
        del outdict[b]
        
    return json.dumps(outdict)
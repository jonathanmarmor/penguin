import random
from weighted_choice import weighted_choice

musicians = ['Erin', 'Laura', 
            'QuentinVoice', 'Quentin', \
            'PhilVoice', 'Phil', 'Will', \
            'MattVoice', 'Matt', 
            'IanVoice', 'Ian', \
            'Katie', 'Beth', 'Jason']

def make_ensembles():
    ensembles = {}
    opts = [_vocal1, _vocal2, _vocal3, _inst1, _mixed1, _mixed2, _solo]
    weights = [7,6,5,6,5,3,3]

    for x in range(1,5):
        ensemble = {}
        ensembles[x] = ensemble
        
        ensemble['melody_on_phrase_type_unison'] = []
        ensemble['melody_on_phrase_unison'] = []
        ensemble['harmonize_melody'] = []
    
        ensemble['simple_melody_on_phrase_type_unison'] = []
        ensemble['simple_melody_on_phrase_unison'] = []
        ensemble['harmonize_simple_melody'] = []
        
        ensemble['baritone_simple_melody_on_phrase_type_unison'] = []
        ensemble['baritone_simple_melody_on_phrase_unison'] = []
        ensemble['baritone_harmonize_simple_melody'] = []

        lead = weighted_choice(opts, weights)
        i = opts.index(lead)
        del weights[i]
        opts.remove(lead)        
        
        lead(ensemble)
        
        _keyboards(ensemble)
        _guitars(ensemble)
        _resting(ensemble)
    return ensembles

def _keyboards(ensemble):
    ensemble['beg_and_end_chords_sustained_on_phrase_type'] = []
    ensemble['beg_and_end_chords_sustained_on_phrase'] = []
    
    phil_drone = random.choice([True, False, False, False, False, False])
    if phil_drone:
        phil_only = random.choice([True, True, False])
        if phil_only:
            ensemble['drone'] = ['Phil']
        else:
            ensemble['drone'] = ['Phil', 'Will']
    else:        
        ensemble['drone'] = ['Will']

    keyz = ['Quentin', 'Phil', 'Will']
    playing = _get_playing(ensemble)
    keyz = [k for k in keyz if k not in playing]

    funcs = ['beg_and_end_chords_sustained_on_phrase_type', 'beg_and_end_chords_sustained_on_phrase']
    for m in keyz:
        f = random.choice(funcs)
        ensemble[f].append(m)



    
def _vocal1(ensemble):
    # number 1
    _lead_vocal1(ensemble)
    isresponse = random.choice([True,True,True,True,True,False])
    if isresponse:
        _response1(ensemble)    
    
def _lead_vocal1(ensemble):
    lead = random.choice(['Erin', 'Erin', 'Erin', 'Laura'])
    if lead == 'Erin': harm = 'Laura'
    if lead == 'Laura': harm = 'Erin'
    funcs = ['melody_on_phrase_type_unison'] + (['melody_on_phrase_unison'] * 4)
    f = random.choice(funcs)
    ensemble[f].append(lead)
    ensemble['harmonize_melody'].append(harm)



    
def _response1(ensemble):
    chorus = ['QuentinVoice','PhilVoice','MattVoice','IanVoice']
    playing = _get_playing(ensemble)
    chorus = [c for c in chorus if c not in playing]

    len_chorus = len(chorus)
    if len_chorus == 4:
        num_harm = random.choice([0,0,1,1,1,1,1,1,1,1,1,2])
        if num_harm == 0:
            num_lead_weights = ([1]*8)+([2]*10)+([3]*3)+[4]
        elif num_harm == 1:
            num_lead_weights = ([1]*8)+([2]*10)+([3]*3)
        elif num_harm == 2:
            num_lead_weights = [1,2]
    if len_chorus == 3:
        num_harm = random.choice([0,0,1,1,1,1,1,1,1,1,1,2])
        if num_harm == 0:
            num_lead_weights = ([1]*8)+([2]*10)+([3]*3)
        elif num_harm == 1:
            num_lead_weights = ([1]*8)+([2]*10)
        elif num_harm == 2:
            num_lead_weights = [1]
    if len_chorus == 2:
        num_harm = random.choice([0,0,1,1,1,1,1,1,1,1,1])
        if num_harm == 0:
            num_lead_weights = ([1]*8)+([2]*10)
        elif num_harm == 1:
            num_lead_weights = [1]
    if len_chorus == 1:
        funcs = (['baritone_simple_melody_on_phrase_type_unison'] * 3) + ['baritone_simple_melody_on_phrase_unison']
        f = random.choice(funcs)
        ensemble[f] = chorus
        return None
    if len_chorus == 0:
        return None
    
    num_lead = random.choice(num_lead_weights)
    lead_chorus = random.sample(chorus, num_lead)
    remaining = [c for c in chorus if c not in lead_chorus]
    harm_chorus = random.sample(remaining, num_harm)
    
    funcs = (['baritone_simple_melody_on_phrase_type_unison'] * 3) + ['baritone_simple_melody_on_phrase_unison']
    f = random.choice(funcs)
    ensemble[f] = lead_chorus
    
    ensemble['baritone_harmonize_simple_melody'] = harm_chorus
        


def _vocal2(ensemble):
    # number 2
    melody = random.choice(['Erin', 'Erin', 'Erin', 'Laura'])
    if melody == 'Erin': simple = 'Laura'
    if melody == 'Laura': simple = 'Erin'
    mel_funcs = ['melody_on_phrase_type_unison'] + ['melody_on_phrase_unison'] * 4
    mel_f = random.choice(mel_funcs)
    ensemble[mel_f].append(melody)
    simp_funcs = ['simple_melody_on_phrase_type_unison'] + ['simple_melody_on_phrase_unison']
    simp_f = random.choice(simp_funcs)
    ensemble[simp_f].append(simple)
    
    chorus = ['QuentinVoice','PhilVoice','MattVoice','IanVoice']
    playing = _get_playing(ensemble)
    chorus = [c for c in chorus if c not in playing]
    
    if len(chorus) > 1:
        num_mel_harm = random.choice([0,1,1,1,1,1,1,1,2])
        ensemble['harmonize_melody'] = random.sample(chorus, num_mel_harm)    

    chorus = [c for c in chorus if c not in ensemble['harmonize_melody']]
    if len(chorus) > 1:
        num_simp_harm = random.choice([0,1,1,1,1,1,1,1,2])
        ensemble['harmonize_simple_melody'] = random.sample(chorus, num_simp_harm)    



def _vocal3(ensemble):
    # number 3
    funcs = ['melody_on_phrase_type_unison'] + ['melody_on_phrase_unison'] * 4
    f = random.choice(funcs)
    ensemble[f] = ['Erin', 'Laura']
    
    harms = ['QuentinVoice','PhilVoice','MattVoice','IanVoice']#,'Quentin','Katie']
    num = random.choice([0,1,1,1,1,1,1,1,1,1,1,2,2,2])
    ensemble['harmonize_melody'] = random.sample(harms,num)

def _inst1(ensemble):
    # number 4
    funcs = ['melody_on_phrase_type_unison', \
             'melody_on_phrase_unison', 'melody_on_phrase_unison']
    f = random.choice(funcs)
    if random.choice([True,True,True,False]):
        ensemble[f] = ['Katie']
    else:
        ensemble[f] = ['Katie', 'Quentin']
 
    lead = random.choice(['Beth','Jason'])
    if lead == 'Beth': harm = 'Jason'
    if lead == 'Jason': harm = 'Beth'
    funcs = (['simple_melody_on_phrase_type_unison'] * 2) + ['simple_melody_on_phrase_unison']
    f = random.choice(funcs)
    ensemble[f].append(lead)
    ensemble['harmonize_simple_melody'].append(harm)

def _mixed1(ensemble):
    # number 5
    lead_f = random.choice([_lead_vocal1, _vocal3])
    lead_f(ensemble)
    
    simp = ['Katie', 'Quentin', 'Beth', 'Jason']
    
    simp_f = random.choice(['simple_melody_on_phrase_type_unison', \
                            'simple_melody_on_phrase_unison'])
    num_simp_lead = random.choice([1,1,2])
    ensemble[simp_f] = random.sample(simp, num_simp_lead)
    
    simp = [s for s in simp if s not in ensemble[simp_f]]
    num_simp_harm = random.choice([1,1,1,1,1,2])
    ensemble['harmonize_simple_melody'] = random.sample(simp, num_simp_harm)    
    
def _mixed2(ensemble):
    # number 6
    solo = ['Katie', 'Quentin', 'Beth', 'Jason']
    weights = [7,3,2,2]
    s = weighted_choice(solo, weights)
    
    funcs = ['melody_on_phrase_type_unison'] + (['melody_on_phrase_unison'] * 3)
    f = random.choice(funcs)
    ensemble[f].append(s)
    solo.remove(s)
    if random.choice([False,False,True]):
        s2 = random.choice(solo)
        ensemble[f].append(s2)
        solo.remove(s2)
    
    if random.choice([True,False]):
        h = random.choice(solo)
        ensemble['harmonize_melody'].append(h)
        solo.remove(h)
        if random.choice([False,False,False,True]):
            h2 = random.choice(solo)
            ensemble['harmonize_melody'].append(h2)
    
    simp_funcs = ['simple_melody_on_phrase_type_unison', 'simple_melody_on_phrase_unison']
    f = random.choice(simp_funcs)
    ensemble[f] = ['Erin', 'Laura']
    
    harms = ['QuentinVoice','PhilVoice','MattVoice','IanVoice']
    num = random.choice([0,1,1,1,1,1,1,1,1,1,1,2,2,2])
    ensemble['harmonize_simple_melody'] = random.sample(harms,num)    
    

def _solo(ensemble):
    # number 7
    dudes = ['Erin', 'Laura', 'Katie', 'Quentin', 'Beth', 'Jason']
    
    func_type = random.choice(['melody', 'simple'])
    if func_type == 'melody':
        funcs = ['melody_on_phrase_type_unison', 'melody_on_phrase_unison']
    else:
        funcs = ['simple_melody_on_phrase_type_unison', 'simple_melody_on_phrase_unison']
    f = random.choice(funcs)
    s = random.choice(dudes)
    ensemble[f] = [s]
    dudes.remove(s)
    if random.choice([True,False,False,False]):
        s2 = random.choice(dudes)
        ensemble[f].append(s2)
        dudes.remove(s2)
        if random.choice([True,False,False,False]):
            s3 = random.choice(dudes)
            ensemble[f].append(s3)
            dudes.remove(s3)
    
    if func_type == 'melody':
        f = 'harmonize_melody'
    else:
        f = 'harmonize_simple_melody'
    h = random.choice(dudes)
    dudes.remove(h)
    ensemble[f] = [h]
    if random.choice([True,False,False,False,False,False]):
        h2 = random.choice(dudes)
        ensemble[f].append(h2)
    
    
    
    
    
    
    
    
    

def _guitars(ensemble):
    weights = [0] + ([1]*4) + ([2]*14)
    num_guitars = random.choice(weights)
    ensemble['guitar_chords_on_phrase_type_unison'] = []
    ensemble['guitar_chords_on_phrase_unison'] = []
    ensemble['guitar_chords_on_phrase_type'] = []
    ensemble['guitar_chords_on_phrase'] = []
    guitarists = ['Matt','Ian']    
    if num_guitars == 1:
        g = random.choice(guitarists)
        funcs = ['guitar_chords_on_phrase_type', 'guitar_chords_on_phrase']
        f = random.choice(funcs)
        ensemble[f].append(g)
    elif num_guitars == 2:
        if random.choice([True, False]):
            # unison
            funcs = ['guitar_chords_on_phrase_type_unison', 'guitar_chords_on_phrase_unison']
            f = random.choice(funcs)
            ensemble[f] = guitarists
        else:
            # not unison
            funcs = ['guitar_chords_on_phrase_type', 'guitar_chords_on_phrase']
            for g in guitarists:
                f = random.choice(funcs)
                ensemble[f].append(g)

def _resting(ensemble):
    ensemble['resting'] = []
    playing = _get_playing(ensemble)
    for m in musicians:
        if m not in playing:
            ensemble['resting'].append(m)

def _get_playing(ensemble):
    playing = []
    for k in ensemble:
        for m in ensemble[k]:
            playing.append(m)
    return playing


    
    

if __name__ == '__main__':
    for x in range(100):
        es = make_ensembles()
        for k in es:
            e = es[k]
            if len(_get_playing(e)) != 14:
                print
                print '-'* 40
                print
                for key in e:
                    print '{0:<40}{1}'.format(key, e[key])
        
    
##    es = make_ensembles()
##    for k in es:
##        e = es[k]
##        print '-'*15
##        for k in e:
##            print '{0:<40}{1}'.format(k, e[k])
##        print
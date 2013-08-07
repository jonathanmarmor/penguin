import random
from piece.weighted_choice import weighted_choice



def make_ensembles():
    musicians = ['Emma', 'Paul', 'Katie', 'Christine', 'Mark', 'Michael', 'James']
    ensembles = {}
    for x in range(1,4):
        ensembles[x] = _make_ensemble()
        print
        print 'Ensemble ', x
        for mn in ensembles[x]:
            print '{0:<50}{1}'.format(mn, ensembles[x][mn])
        print
        
    
    return ensembles

def _make_ensemble():
    ensemble = {}
    mel_type, acc_type = _get_role_types()
    mel_parts, acc_parts = _types_to_parts(mel_type, acc_type)
    
    mel_insts, acc_insts = _choose_inst_mel_acc(mel_parts)
    _assign_acc_musicians(ensemble, acc_parts, acc_insts)
    
    #_strumming(ensemble)
    
    _assign_mel_musicians(ensemble, mel_parts, mel_insts)
    _resting(ensemble)

    return ensemble
        
        
def _get_role_types():
    all_ens = {
        ('mel','dynamic'):75,
        ('melharm','dynamic'):1000,
        ('simpmel','dynamic'):50,
        ('simpmelharm','dynamic'):150,
        ('mel-simpmel','dynamic'):100,
        ('mel-simpmelharm','dynamic'):1000,
        ('melharm-simpmel','dynamic'):200,
        ('melharm-simpmelharm','dynamic'):100,
        ('none','dynamic'):20,  
        
        ('mel','continuous'):150,
        ('melharm','continuous'):1750,
        ('simpmel','continuous'):100,
        ('simpmelharm','continuous'):200,
        ('mel-simpmel','continuous'):500,
        ('mel-simpmelharm','continuous'):1250,
        ('melharm-simpmel','continuous'):1500,
        ('melharm-simpmelharm','continuous'):1100,
        ('none','continuous'):40,
        
        ('mel','intermittent'):5,
        ('melharm','intermittent'):37,
        ('simpmel','intermittent'):2,
        ('simpmelharm','intermittent'):10,
        ('mel-simpmel','intermittent'):7,
        ('mel-simpmelharm','intermittent'):50,
        ('melharm-simpmel','intermittent'):12,
        ('melharm-simpmelharm','intermittent'):25,
        ('none','intermittent'):1, 
        
        ('mel','none'):3,
        ('simpmel','none'):3,
        ('mel-simpmel','none'):1,
    }
    
    
##    melody_type_opts = {
##        'mel':10,
##        'melharm':26,
##        'simpmel':10,
##        'simpmelharm':24,
##        'mel-simpmel':2,
##        'mel-simpmelharm':15,
##        'melharm-simpmel':2,
##        'melharm-simpmelharm':2,
##        'none':9
##    }

    ensemble_type = weighted_choice(all_ens.keys(), all_ens.values())
    melody_type = ensemble_type[0]
    accompaniment_type = ensemble_type[1]
    
    
##    melody_type = weighted_choice(melody_type_opts.keys(), melody_type_opts.values())
##
##    accs_all = ['dynamic','continuous', 'intermittent','none']
##    accs_no_none = ['dynamic','continuous', 'intermittent']
##    melody_type_accompaniment_type_opts = {
##        'mel':accs_all,
##        'melharm':accs_no_none,
##        'simpmel':accs_all,
##        'simpmelharm':accs_no_none,
##        'mel-simpmel':accs_no_none,
##        'mel-simpmelharm':accs_no_none,
##        'melharm-simpmel':accs_no_none,
##        'melharm-simpmelharm':accs_no_none,
##        'none':accs_no_none
##    }
##
##    accompaniment_type_weights_ALL = {
##        'dynamic':48,
##        'continuous':25,
##        'intermittent':20,
##        'none':7
##    }
##
##    acc_type_opts = melody_type_accompaniment_type_opts[melody_type]
##    acc_type_weights = []    
##    for opt in acc_type_opts:
##        acc_type_weights.append(accompaniment_type_weights_ALL[opt])
##        
##    accompaniment_type = weighted_choice(acc_type_opts, acc_type_weights)
##    
    return melody_type, accompaniment_type

def _types_to_parts(mel, acc):
    melody_types_ensemble_roles = {
        'mel':['melody_on_phrase_unison'],
        'melharm':['melody_on_phrase_unison','harmonize_melody'],
        'simpmel':['simple_melody_on_phrase_unison'],
        'simpmelharm':['simple_melody_on_phrase_unison','harmonize_simple_melody'],
        'mel-simpmel':['melody_on_phrase_unison','simple_melody_on_phrase_unison'],
        'mel-simpmelharm':['melody_on_phrase_unison','simple_melody_on_phrase_unison','harmonize_simple_melody'],
        'melharm-simpmel':['melody_on_phrase_unison','harmonize_melody','simple_melody_on_phrase_unison'],
        'melharm-simpmelharm':['melody_on_phrase_unison', 'harmonize_melody','simple_melody_on_phrase_unison','harmonize_simple_melody'],
        'none':[]
    }
    accompaniment_types_ensemble_roles = {
        'dynamic':['chords_sustained_on_phrase','beg_and_end_chords_sustained_on_phrase'],
        'continuous':['chords_sustained_on_phrase'],
        'intermittent':['beg_and_end_chords_sustained_on_phrase'],
        'none':[]
    }
    
    return melody_types_ensemble_roles[mel], accompaniment_types_ensemble_roles[acc]

def _choose_inst_mel_acc(mel_parts):
    len_mel_parts = len(mel_parts)
    if len_mel_parts < 3:    
        mel = ['Emma', 'Paul', 'Christine']
        acc = []
        if weighted_choice([True, False],[55,45]):
            mel.append('Katie')
        else:
            acc.append('Katie')
        if weighted_choice([True, False],[10,90]):
            mel.append('Mark')
        else:
            acc.append('Mark')
        acc.extend(['Michael', 'James'])
    elif len_mel_parts == 3:
        num_mels = random.choice([3,3,3,4,4,5])
        possible_mels = ['Emma', 'Paul', 'Christine','Katie', 'Mark']
        mel = random.sample(possible_mels, num_mels)
        for mel_ins in mel:
            possible_mels.remove(mel_ins)
            
        acc = possible_mels + ['Michael', 'James']
##        optionals = ['Katie', 'Mark']
##        to_mel = weighted_choice(optionals, [90,10])
##        mel.append(to_mel)
##        optionals.remove(to_mel)
##        optionals = optionals[0]
##        if random.choice([True, False, False, False, False, False, False, False, False]):
##            mel.append(optionals)
##        else:
##            acc.append(optionals) 
##        acc.extend(['Michael', 'James'])     
    else:        
        mel = ['Emma', 'Paul', 'Christine']
        acc = ['Michael', 'James']
        for inst in ['Katie', 'Mark']:
            if random.choice([True, False]):
                mel.append(inst)
            else:
                acc.append(inst)
    return mel, acc


def _assign_acc_musicians(ensemble, acc_parts, acc_insts):
    for part in acc_parts:
        inst = random.choice(acc_insts)
        acc_insts.remove(inst)
        ensemble[part] = [inst]
    len_acc_insts = len(acc_insts)
    if len_acc_insts > 0 and acc_parts:
        # decide how many of the remaining insts to add 
        # then start adding them randomly between parts
        weights = [(x + 1)** 1.5 for x in range(len_acc_insts + 1)]
        num_insts_to_add = weighted_choice(range(len_acc_insts + 1), weights)
        if num_insts_to_add:
            for x in range(num_insts_to_add):
                chosen_inst = random.choice(acc_insts)
                acc_insts.remove(chosen_inst)
                part = random.choice(acc_parts)
                ensemble[part].append(chosen_inst)

##def _strumming(ensemble):
##    """if there are instruments in the 'chords_sustained_on_phrase' part
##    then choose some number of these instruments between 0 and all
##    to re-assign to the 'guitar_chords_on_phrase' part
##    """
##    if 'chords_sustained_on_phrase' in ensemble:
##        ensemble['guitar_chords_on_phrase'] = []
##        num_insts_opts = range(0, len(ensemble['chords_sustained_on_phrase']) + 1)
##        insts_to_change = random.choice(num_insts_opts)
##        for x in range(insts_to_change):
##            chosen = random.choice(ensemble['chords_sustained_on_phrase'])
##            ensemble['guitar_chords_on_phrase'].append(chosen)
##            ensemble['chords_sustained_on_phrase'].remove(chosen)
                
def _assign_mel_musicians(ensemble, mel_parts, mel_insts):
    for part in mel_parts:
        inst = random.choice(mel_insts)
        mel_insts.remove(inst)
        ensemble[part] = [inst]
    len_mel_insts = len(mel_insts)
    if len_mel_insts > 0 and mel_parts:
        # then maybe add some more insts to the melody and simple melody parts        
        melodies = []
        if 'melody_on_phrase_unison' in mel_parts:
            melodies.append('melody_on_phrase_unison')
        if 'simple_melody_on_phrase_unison' in mel_parts:
            melodies.append('simple_melody_on_phrase_unison')
        if melodies:
            # decide how many of the remaining insts to add 
            # then start adding them randomly between members of melodies
            weights = [(x + 1)** 1.5 for x in range(len_mel_insts + 1)]
            num_insts_to_add = weighted_choice(range(len_mel_insts + 1), weights)
            if num_insts_to_add:
            
            #num_insts_to_add = random.choice(range(len_mel_insts))
                for x in range(num_insts_to_add):
                    chosen_inst = random.choice(mel_insts)
                    mel_insts.remove(chosen_inst)
                    part = random.choice(melodies)
                    ensemble[part].append(chosen_inst)
              

def _resting(ensemble):
    ensemble['resting'] = []
    playing = _get_playing(ensemble)
    musicians = ['Emma', 'Paul', 'Katie', 'Mark', 'Michael', 'James']
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

import random
import sys


class Procedural:

    def __init__(self) :
        self.seed = random.randrange(int(sys.maxsize/8000))
        random.seed(self.seed)
        self.scales = {'minor scales':{'aeolian': [2, 1, 2, 2, 1, 2, 2],      
                                'blues_minor': [3, 2, 1, 1, 3, 2],
                                'dorian': [2, 1, 2, 2, 2, 1, 2]},

                'major scales':{'mixolydian': [2, 2, 1, 2, 2, 1, 2],
                                'blues_major': [2, 1, 1, 3, 2, 3],
                                'natural_major': [2, 2, 1, 2, 2, 2, 1]}
                }

        self.mM_scales = random.choice(['major scales', 'minor scales'])

        self.chords_form = [0, 2, 4]
        self.tonalities = {'non-blues': [[0, 5, 3, 4], 
                                    [5]],
                    'blues': [[0, 4],
                                [0, 3, 4]
                    ]}

        self.scale = []
        self.scale_name = random.choice(list(self.scales[self.mM_scales].keys()))
        self.scale_chords = []
        self.progression = []
        self.f_pitch = 0


######################################-----------------------------------############################################


    def make_chords(self, scale=[], scale_form = 0):
        chords = []
        chords_pila = []
        count = 0
        for s in range(len(scale)):
            if count >= (scale_form - 1):
                chords.append(chords_pila)
                chords_pila = []
                count = 0
            else:
                try:
                    pila = []
                    for c in self.chords_form:
                        pila.append(scale[s + c])
                    chords_pila.append(pila)
                    count += 1
                except:
                    pass
            
        return chords



    def string_notes(self, pitch = 4):
        notes = [] 
        pila = []
        pila.append(pitch)

        scale = self.scales[self.mM_scales][self.scale_name]


        for _ in range(0, 11):
            if not pila:
                pila.append(notes[-1][-1] + scale[-1])
            for s in range(len(scale) - 1):
                note = pila[-1] + scale[s]
                if note <= 127:
                    pila.append(note)
            notes.append(pila)
            pila = []

        
        flat_str_notes = [item for sublist in notes for item in sublist]
        scale_chords = self.make_chords(scale=flat_str_notes, scale_form = len(notes[0]))


        return [notes, scale_chords]



    def make_progression(self, scale_name):
        progresion = []
        tonality = []

        if 'blues' in scale_name:
            tonality = random.choice(self.tonalities['blues'])
        else:
            blues = random.choice(list(self.tonalities.keys()))
            tonality = random.choice(self.tonalities[blues])
        
        for i in range(8):
            if len(tonality) == 1:
                for i in range(8):
                    progresion.append(0)
                return progresion

            if i == 0:
                progresion.append(tonality[0])
            elif i > 0 and i <= 3:
                prob = random.uniform(0, 1)
                if prob >= 0.5:
                    progresion.append(tonality[0])
                else:
                    tonal = random.choice(tonality[-(len(tonality) - 2):])
                    progresion.append(tonal)
            elif i >= 4:
                tonal = random.choice(tonality)
                progresion.append(tonal)
            
        if progresion[-1] != 0:
            progresion[-1] = 0

        return progresion

    def make_bass(self, rythm):
        bass_compas = []

        p_count = 0
        for r in range(len(rythm)):
            compas = []

            if p_count >= 7:
                p_count = 0

            for n in rythm[r]:
                if p_count == 3 or p_count == 7:
                    fifth = bool(random.getrandbits(1))
                    if fifth:
                        compas.append(self.scale_chords[2][self.progression[p_count]][-1])
                    else:
                        compas.append(self.scale_chords[2][self.progression[p_count]][0])
                elif p_count == 2 or p_count == 6:
                    compas.append(self.scale_chords[2][self.progression[p_count]][1])
                else:
                    compas.append(self.scale_chords[2][self.progression[p_count]][0])
            bass_compas.append(compas)
            p_count += 1


        return bass_compas

    def make_guitar(self, rythm, min_len=0, leads=False):
        guitar_notes = []
        prog_count = 0
        random_octave = random.randint(4, 6)

        if leads:
            print('LEADS')
            for r in rythm:
                if prog_count >= 8:
                    prog_count = 0
                compas = []
                for i in range(len(r)):
                    r_note = 0
                    if i == 0:
                        r_note = self.scale_chords[2][self.progression[prog_count]][0]
                    else:
                        random_note = random.randint(0, 2)
                        r_note = self.scale_chords[random_octave][self.progression[prog_count]][random_note]
                    
                    l = int(r[i] / min_len)
                    for _ in range(l):
                        compas.append(r_note)

                guitar_notes.append(compas)
                prog_count += 1


        else:
            for r in rythm:
                if prog_count >= 8:
                    prog_count = 0
                compas = []
                for i in range(len(r)):
                    if i == 0:
                        compas.append(self.scale_chords[2][self.progression[prog_count]][0])
                    else:
                        random_note_pos = random.randint(0, 2)
                        rand_note = self.scale_chords[random_octave][self.progression[prog_count]][random_note_pos]        
                        compas.append(rand_note)
                guitar_notes.append(compas)
                prog_count += 1


        return guitar_notes


    def Fundamental(self):
        kick_penta = []
        snare_penta = []
        hh_penta = []
        cimbal_penta = []
        guitar = []

        #Epic mood defaults
        blacks = 2
        figure = random.randint(4, 5)

        #Building fundamental rythm
        for _ in range(1):
            for i in range(4):
                compas = []
                sum_compas = 0

                for j in range(4):                
                    
                    nota = 1/pow(2, random.randrange(blacks, figure))
                    nota = nota/0.25

                    #White notes
                    if nota == 2.0:
                        compas.append(nota)
                    
                    #Black notes
                    if nota == 1.0:
                        compas.append(nota)

                    #1/8 notes
                    if nota == 0.5:
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    #1/16 notes
                    if nota == 0.25:
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    #1/32 notes
                    if nota == 0.125:
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        compas.append(nota)
                        j += 1
                    
                    sum_compas = sum(compas)
                    
                    #Breaking if 4/4
                    if sum_compas >= 4.0:
                        i += 1
                        break
                
                kick_penta.append(compas)
            
            #Repeating for 8 bars
            for p in kick_penta[-4:]:
                kick_penta.append(p)

        for i in range(len(kick_penta)):
            guitar.append(kick_penta[i].copy()) 

        #Choice of snare: 0 for snare in 2 and 4, 1 for snare in 3
        snare_beats = bool(random.getrandbits(1))

        #Building hi-hat, snare and silenced cimbal
        for i in range(len(kick_penta)):
            hh_compas = []
            snare_compas = []
            cimbal_compas = []
            for j in range(4):
                hh_compas.append(1.0)
                cimbal_compas.append(-1.0)
                if not snare_beats:
                    if j == 1 or j == 3:
                        snare_compas.append(1.0)
                        try:
                            kick_penta[i][j] *= -1
                        except:
                            pass
                    else:
                        snare_compas.append(-1)
                else:
                    if j == 2:
                        snare_compas.append(1.0)
                        kick_penta[i][j] *= -1
                    else:
                        snare_compas.append(-1)

            #Appending instruments
            hh_penta.append(hh_compas)
            snare_penta.append(snare_compas)
            cimbal_penta.append(cimbal_compas)
    

        #Reducing 1/32 for acentuation in kick
        for i in range(len(guitar)):
            for j in range(len(guitar[i])):
                try:
                    if guitar[i][j] == 0.125 and guitar[i][j] == guitar[i][j + 1]:
                        guitar[i][j] = 0.25 
                        del guitar[i][j + 1]
                except:
                    pass



        fundamental_rythm = {'string': {'guitar': guitar}, 
                    'perc': {'kick': kick_penta, 
                                'hhat': hh_penta,
                                'snare': snare_penta,
                                'cimbal': cimbal_penta}}


        return fundamental_rythm

    def composer(self):
        self.scale, self.scale_chords = self.string_notes(pitch = random.randint(0, 11))
        self.progression = self.make_progression(self.scale_name)

        fund = self.Fundamental()
        leads = bool(random.getrandbits(1))

        bass = self.make_bass(fund['perc']['kick'])
        

        if leads:
            lead_rythm = []

            mins = []
            for i in fund['perc']['kick']:
                mins.append(min(i))
            
            min_len = min(mins)


            for _ in range(len(fund['string']['guitar'])):
                compas = []
                for i in range(int(4.0/min_len)):
                    compas.append(min_len)
                lead_rythm.append(compas)
            
            guitar = self.make_guitar(fund['string']['guitar'], min_len=min_len, leads=leads)

            song = {'string': 
                        {'guitar_notes': guitar, 
                         'rythm': lead_rythm,
                         'bass_notes': bass,
                         'bass_rythm': fund['perc']['kick']}}
            song['perc'] = fund['perc']
        
        else:
            guitar = self.make_guitar(fund['string']['guitar'])
            song = {'string': 
                            {'guitar_notes': guitar, 
                             'rythm': fund['string']['guitar'],
                             'bass_notes': bass,
                             'bass_rythm': fund['perc']['kick']}}
            song['perc'] = fund['perc']

        return song
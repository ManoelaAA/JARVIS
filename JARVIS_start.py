def JARVIS_start(hour):

    JARVIS_speech = ''

    print(hour)

    if hour >= 6 and hour <= 12:
        JARVIS_speech = 'Bom dia'

    if hour > 12 and hour < 18:
        JARVIS_speech = 'Boa tarde'

    if hour >= 18 and hour > 0:
        JARVIS_speech = 'Boa noite'

    if hour >= 0 and hour < 5:
        JARVIS_speech = 'Boa noite'

    return JARVIS_speech
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try { $synth.SelectVoice('Microsoft Zira Desktop') } catch {}
$synth.Rate = 3
$synth.SetOutputToWaveFile('C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/saturday_reel_build/s1.wav')
$synth.Speak('Stop missing secret eggs! Today is Saturday Admin Abuse with 2X luck on Roblox Steal An Egg!')
$synth.SetOutputToWaveFile('C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/saturday_reel_build/s2.wav')
$synth.Speak('Track every secret and divine spawn live across 12 biomes before the crowds arrive!')
$synth.SetOutputToWaveFile('C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/saturday_reel_build/s3.wav')
$synth.Speak('Our live radar predicts the exact wave countdown with 94 percent accuracy!')
$synth.SetOutputToWaveFile('C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/saturday_reel_build/s4.wav')
$synth.Speak('Turn on Audio Sniper to hear instant sound chimes the second your target egg spawns!')
$synth.SetOutputToWaveFile('C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/saturday_reel_build/s5.wav')
$synth.Speak('Event starts at 15 hundred UTC! Open egg stock dot xyz right now! Link in pinned comment!')
$synth.Dispose()
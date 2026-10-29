Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try { $synth.SelectVoice('Microsoft Zira Desktop') } catch {}
$synth.Rate = 2

$outDir = "C:/Users/jyoti/OneDrive/Discord Bots/steal_an_egg/today_viral_short"

$synth.SetOutputToWaveFile("$outDir/part1.wav")
$synth.Speak("Stop wasting hours waiting at empty nests in Steal An Egg! Over 670,000 players are online right now, but almost nobody knows when Secret and Divine eggs actually spawn!")

$synth.SetOutputToWaveFile("$outDir/part2.wav")
$synth.Speak("Eggs don't drop randomly! They follow an exact wave cadence. EggStock dot xyz is the live 24/7 radar tracking all 12 biomes across active Roblox servers in real time!")

$synth.SetOutputToWaveFile("$outDir/part3.wav")
$synth.Speak("Our AI Forecaster gives you sub-second countdowns! Plus, use the Target Sniper to hear an instant siren chime the second Kitsune, Nightflame, or Aetheron appears!")

$synth.SetOutputToWaveFile("$outDir/part4.wav")
$synth.Speak("Never miss a Divine drop again! Open egg stock dot xyz right now and join over 1,600 players in our Discord! Link in pinned comment and description!")

$synth.Dispose()
Write-Host "Audio generated successfully!"

# NaverTTS
NaverTTS using papago
## Method
1.Insert text in papago and press "Listening pronunciation" Button</br>
2.Fetch network requests and find audio url in header using content-type</br>
3.Save audio url to file

## How to use
```
from tts import NaverTTS
tts = NaverTTS()
tts.save(text, path)
```
text and path must be a string

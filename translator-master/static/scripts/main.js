$(function() {
  $("#translate").on("click", function (e) {
    e.preventDefault();
    var translateVal = document.getElementById("text-to-translate").value;
    var languageVal = document.getElementById("select-language").value;
    var translateRequest = {'text': translateVal, 'to': languageVal}

    if (translateVal !== "") {
      $.ajax({
        url: '/translate-text',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        dataType: 'json',
        data: JSON.stringify(translateRequest),
        success: function (data) {
          for (var i = 0; i < data.length; i++) {
            document.getElementById("translation-result").textContent = data[i].translations[0].text;
            document.getElementById("detected-language-result").textContent = data[i].detectedLanguage.language;
            if (document.getElementById("detected-language-result").textContent !== "") {
              document.getElementById("detected-language").style.display = "block";
            }
            document.getElementById("confidence").textContent = data[i].detectedLanguage.score;
          }
        }
      });
    }
    ;
  });
  $("#text-to-speech").on("click", function (e) {
    e.preventDefault();
    var ttsInput = document.getElementById("translation-result").value;
    var ttsVoice = document.getElementById("select-voice").value;
    var ttsRequest = {'text': ttsInput, 'voice': ttsVoice}

    var xhr = new XMLHttpRequest();
    xhr.open("post", "/text-to-speech", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.responseType = "blob";
    xhr.onload = function (evt) {
      if (xhr.status === 200) {
        audioBlob = new Blob([xhr.response], {type: "audio/mpeg"});
        audioURL = URL.createObjectURL(audioBlob);
        if (audioURL.length > 5) {
          var audio = document.getElementById("audio");
          var source = document.getElementById("audio-source");
          source.src = audioURL;
          audio.load();
          audio.play();
        } else {
          console.log("An error occurred getting and playing the audio.")
        }
      }
    }
    xhr.send(JSON.stringify(ttsRequest));
  });

  $('select[id="select-language"]').change(function (e) {
    if ($(this).val() == "zh-Hans") {
      document.getElementById("select-voice").value = "(zh-HK, Tracy, Apollo)";
    }
    if ($(this).val() == "zh-Hant") {
      document.getElementById("select-voice").value = "(zh-HK, Tracy, Apollo)";
    }
    if ($(this).val() == "hr") {
      document.getElementById("select-voice").value = "(hr-HR, Matej)";
    }
    if ($(this).val() == "en") {
      document.getElementById("select-voice").value = "(en-US, Jessa24kRUS)";
    }
    if ($(this).val() == "fr") {
      document.getElementById("select-voice").value = "(fr-FR, HortenseRUS)";
    }
    if ($(this).val() == "de") {
      document.getElementById("select-voice").value = "(de-DE, HeddaRUS)";
    }
    if ($(this).val() == "el") {
      document.getElementById("select-voice").value = "(el-GR, Stefanos)";
    }
    if ($(this).val() == "he") {
      document.getElementById("select-voice").value = "(he-IL, Asaf)";
    }
    if ($(this).val() == "it") {
      document.getElementById("select-voice").value = "(it-IT, LuciaRUS)";
    }
    if ($(this).val() == "ja") {
      document.getElementById("select-voice").value = "(ja-JP, HarukaRUS)";
    }
    if ($(this).val() == "ko") {
      document.getElementById("select-voice").value = "(ko-KR, HeamiRUS)";
    }
    if ($(this).val() == "pt") {
      document.getElementById("select-voice").value = "(pt-BR, HeloisaRUS)";
    }
    if ($(this).val() == "ru") {
      document.getElementById("select-voice").value = "(ru-RU, EkaterinaRUS)";
    }
    if ($(this).val() == "es") {
      document.getElementById("select-voice").value = "(es-ES, HelenaRUS)";

    }
  });
})
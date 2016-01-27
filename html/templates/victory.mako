<html>
<body style="background-image: url('${base}images/party.png');background-repeat: no-repeat; background-attachment: fixed; background-position: center; background-color: #CB242B; ">
<div id="play" style="text-align: center; line-height: 20vh; font-size: 20vh;" onclick="document.getElementById('audio').play();">&#9658</div>
<audio autoplay id="audio" onplaying="document.getElementById('play').style.visibility = 'hidden';">
  <source src="${base}audio/ussr.mp3" type="audio/mpeg">
</audio>
</body>
</html>
$(function() {
  console.log(imgSrc,imgTotal,pos,remain,progress);
  var ctx = $('#main-canvas')[0].getContext('2d');
  var posText = $('#pos');
  var msgText = $('#message');
  posText.text(parseInt(remain));
  var img = new Image();
  img.onload = function() {
    ctx.canvas.width = img.width;
    ctx.canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
  };
  if(imgSrc !== 'None') {
    img.src = imgSrc;
  } else {
    drawCompleteImage();
  }
  $('.progress-bar').css({'width':progress + '%'});

  $('#next').on('click', function(e) {
    $.getJSON('/clipper/next', function(data) {
      if(parseInt(data.progress) !== 100) {
        img.src = data.imgsrc;
        msgText.text('remain: ' + data.remain);
      } else {
        msgText.text('complete !');
        drawCompleteImage();
      }
      console.log('next',data);
      posText.text(data.remain);
      $('.progress-bar').css({'width':data.progress + '%'});
    });
  });

  $('#previous').on('click', function(e) {
    $.getJSON('/clipper/previous', function(data) {
      if(parseInt(data.progress) !== 100) {
        img.src = data.imgsrc;
        msgText.text('remain: ' + data.remain);
      }
      if(parseInt(data.progress) === 90) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.drawImage(img, 0, 0);
      }
      console.log('prev',data);
      posText.text(data.remain);
      $('.progress-bar').css({'width':data.progress + '%'});
    });
  });

  function drawCompleteImage() {
    // ctx.canvas.width = 450;
    // ctx.canvas.height = 300;
    ctx.rect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.stroke();
    ctx.font = '30px Consolas, sans-serif';
    ctx.fillStyle = '#0099ff';
    ctx.textAlign = 'center';
    ctx.fillText('complete !', ctx.canvas.width/2, ctx.canvas.height/2);
  }
});
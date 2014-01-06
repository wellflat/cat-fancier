$(function() {
  console.log('index.html',imgSrc,imgTotal,pos,remain,progress,message);

  var ctx = $('#main-canvas')[0].getContext('2d'),
      canvas = ctx.canvas,
      img = new Image(),
      coords = null,
      curcoords = null,
      badgeInfo = $('#badge'),
      msgInfo = $('#message');

  $('.progress-bar').css({'width':progress + '%'});
  msgInfo.text(message);

  img.addEventListener('load', function() {
    ctx.canvas.width = img.width;
    ctx.canvas.height = img.height;
    ctx.drawImage(img, 0, 0);

    $('#main-canvas').Jcrop({
      onSelect: function(c) {
        curcoords = c;
      },
      onRelease: function() {
        coords = curcoords;
        ctx.lineWidth = 3;
        ctx.strokeStyle = '#ff0000';
        ctx.strokeRect(curcoords.x, curcoords.y, curcoords.w, curcoords.h);
      }
    });
  }, false);

  if(parseInt(progress) !== 100) {
    img.src = imgSrc;
  } else {
    drawCompleteImage();
    $('#next').toggle();
    $('#prev').toggle();
    msgInfo.text('complete!');
  }

  $('#next').on('click', function(e) {
    console.log('coords',coords);
    coords = JSON.stringify(coords);
    $.getJSON('/clipper/next', {'coords':coords}, function(data) {
      if(parseInt(data.progress) !== 100) {
        img.src = data.imgsrc;
        msgInfo.text('remain: ' + data.remain);
      } else {
        msgInfo.text('complete !');
        drawCompleteImage();
      }
      console.log('next',data);
      badgeInfo.text(data.remain);
      $('.progress-bar').css({'width':data.progress + '%'});
      coords = null;
    });
  });

  $('#prev').on('click', function(e) {
    coords = JSON.stringify(coords);
    $.getJSON('/clipper/prev', {'coords':coords}, function(data) {
      if(parseInt(data.progress) !== 100) {
        img.src = data.imgsrc;
        msgInfo.text('remain: ' + data.remain);
      }
      if(parseInt(data.progress) === 90) {
        ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        ctx.drawImage(img, 0, 0);
      }
      console.log('prev',data);
      badgeInfo.text(data.remain);
      $('.progress-bar').css({'width':data.progress + '%'});
      coords = null;
    });
  });

  $('#reset-progress').on('click', function(e) {
    $.post('/clipper/progress', {'pos':0}, function(data) {
      if(parseInt(data.status) === 200) {
        msgInfo.text('successfully, reset position to zero.');
      }
    });
  });

  $('#create-list').on('click', function(e) {
    $.post('/clipper/list', function(data) {
      msgInfo('successfully, create sample list');
    });
  });

  function drawCompleteImage() {
    ctx.font = '40px Consolas, sans-serif';
    ctx.fillStyle = '#0099ff';
    ctx.textAlign = 'center';
    ctx.fillText('complete !', ctx.canvas.width/2, ctx.canvas.height/2);
  }
});
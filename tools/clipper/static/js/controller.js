$(function() {
  console.log('index.html',imgSrc,imgTotal,pos,status,remain,progress,message);

  var image = $('#main-img'),
      coords = null,
      curcoords = null,
      statusInfo = $('#status'),
      badgeInfo = $('#badge'),
      msgInfo = $('#message'),
      progressBar = $('.progress-bar');

  progressBar.css({'width':progress + '%'});
  badgeInfo.text(remain);
  showIcon(status);

  var jcropAPI = null;
  image.Jcrop({
    onSelect: function(c) {
      curcoords = c;
      msgInfo.text('x:' + c.x + ', y:' + c.y + ', width:' + c.w + ', height:' + c.h);
      console.log(c);
    },
    onRelease: function() {
      coords = curcoords;
      //msgInfo.text(coords.x,coords.y,coords.x2,coords.y2);
      // ctx.lineWidth = 3;
      // ctx.strokeStyle = '#ff0000';
      // ctx.strokeRect(curcoords.x, curcoords.y, curcoords.w, curcoords.h);
    }
  }, function() { jcropAPI = this; });

/*
  img.addEventListener('load', function(e) {
  }, false);
*/

  if(parseInt(progress) !== 100) {
    jcropAPI.setImage(imgSrc);
  } else {
    //drawCompleteImage();
    $('#next').toggle();
    $('#prev').toggle();
    msgInfo.text('complete!');
  }

  $('#next').on('click', function(e) {
    coords = curcoords;
    console.log('coords',coords);
    coords = JSON.stringify(coords);
    $.getJSON('/clipper/next', {'coords':coords}, function(data) {
      if(parseInt(data.progress) !== 100) {
        jcropAPI.setImage(data.imgsrc);
        msgInfo.text(data.imgsrc);
      } else {
        msgInfo.text('complete !');
        statusInfo.css({'display':'none'});
        //drawCompleteImage();
      }
      console.log('next',data);
      badgeInfo.text(data.remain);
      showIcon(data.status);
      progressBar.css({'width':data.progress + '%'});
      coords = curcoords = null;
    });
  });

  $('#prev').on('click', function(e) {
    coords = curcoords;
    coords = JSON.stringify(coords);
    $.getJSON('/clipper/prev', {'coords':coords}, function(data) {
      if(parseInt(data.progress) !== 100) {
        //img.src = data.imgsrc;
        jcropAPI.setImage(data.imgsrc);
        msgInfo.text(data.imgsrc);
      }
      if(parseInt(data.progress) === 90) {
        // ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
        // ctx.drawImage(img, 0, 0);
      }
      console.log('prev',data);
      badgeInfo.text(data.remain);
      showIcon(data.status);
      progressBar.css({'width':data.progress + '%'});
      coords = curcoords = null;
    });
  });

  $('#clear').on('click', function(e) {
    // ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    // ctx.drawImage(img, 0, 0);
    coords = null;
  });

  $('#reset-progress').on('click', function(e) {
    $.post('/clipper/progress', {'pos':0}, function(data) {
      if(parseInt(data.status) === 200) {
        msgInfo.text('successfully, reset position to zero.');
        progressBar.css({'width':'0%'});
      }
    });
  });

  $('#sync-database').on('click', function(e) {
    $.post('/clipper/sync', function(data) {
      msgInfo.text('successfully, sync data');
    });
  });

  function showIcon(status) {
    if(parseInt(status) == 200) {
      statusInfo.css({'color':'#00cc66'});
    } else {
      statusInfo.css({'color':'#aaa'});
    }
  }

  function drawCompleteImage() {
    // ctx.font = '40px Consolas, sans-serif';
    // ctx.fillStyle = '#0099ff';
    // ctx.textAlign = 'center';
    // ctx.fillText('complete !', ctx.canvas.width/2, ctx.canvas.height/2);
  }
});
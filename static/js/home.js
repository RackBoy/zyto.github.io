$(function() {
  /* NOTE: hard-refresh the browser once you've updated this */
  $(".typed").typed({
    strings: [
      "Joel's Website <br/>" +
      "><span class='caret'>$</span> personal profile: Tech enthusiasm, artist, creator <br/> ^100" +
      "><span class='caret'>$</span> studies: Electronic Technologis, Electronic Engineering<br/> ^100" +
      "><span class='caret'>$</span> skills: Software and hardware programmer, enthusiams of neuronal networks, data bases, design of PCBs<br/> ^100" +
      "><span class='caret'>$</span> hobbies: Reading, Writting, Languages, Tech content creator<br/> ^300" 
    ],
    showCursor: true,
    cursorChar: '_',
    autoInsertCss: true,
    typeSpeed: 0.001,
    startDelay: 50,
    loop: false,
    showCursor: false,
    onStart: $('.message form').hide(),
    onStop: $('.message form').show(),
    onTypingResumed: $('.message form').hide(),
    onTypingPaused: $('.message form').show(),
    onComplete: $('.message form').show(),
    onStringTyped: function(pos, self) {$('.message form').show();},
  });
  $('.message form').hide()
});

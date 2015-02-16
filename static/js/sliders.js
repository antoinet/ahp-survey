$(document).ready(function () {

 // init sliders
 $('.slider').each(function() {
   var id = $(this).attr('id');
   $(this).noUiSlider({
     start: [1],
     range: {
      'min':     [ 1/9 ],
      '6.25%':   [ 1/8 ],
      '12.5%':   [ 1/7 ],
      '18.75%':  [ 1/6 ],
      '25%':     [ 1/5 ],
      '31.25%':  [ 1/4 ],
      '37.5%':   [ 1/3 ],
      '43.75%':  [ 1/2 ],
      '50%':     [ 1 ],
      '56.25%':  [ 2 ],
      '62.5%':   [ 3 ],
      '68.75%':  [ 4 ],
      '75%':     [ 5 ],
      '81.25%':  [ 6 ],
      '87.5%':   [ 7 ],
      '93.75%':  [ 8 ],
      'max':     [ 9 ], 
     },
     direction: "rtl",
     format: wNumb({decimals: 6}),
     snap: true
   });
   $(this).Link('lower').to(id);
   $(this).css('margin-bottom', '40px');
 });

 $('.slider').noUiSlider_pips({
   mode: 'positions',
   values: [0, 6.25, 12.5, 18.75, 25, 31.25, 37.25, 43.75, 50, 56.25, 62.5, 68.75, 75, 81.25, 87.5, 93.75, 100],
   density: 8,
   filter: function(value, type) { return 0; }
 });
});


function reset_sliders() {
  if (confirm('Wollen Sie wirklich alle Regler zurücksetzen?')) {
    $('.slider').val(1);
  }
}

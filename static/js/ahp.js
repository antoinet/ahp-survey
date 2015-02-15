  random_inconsistency_indices = [0.00,
	  0.00, 0.00, 0.58, 0.90, 1.12,
	  1.24, 1.32, 1.41, 1.45, 1.49,
	  1.51, 1.48, 1.56, 1.57, 1.59
  ];

  matrix = {
    'abs': [],
    'norm': []
  };
  for (var i = 0; i < goals.length; i++) {
    matrix['abs'][i] = [];
    matrix['norm'][i] = [];
    matrix['abs'][i][i] = 1;
    matrix['norm'][i][i] = 1;
  }

  weights = [];
  consistency_vector = [];
  consistency_ratio = undefined;

  function populate_matrix() {
    for (var i = 0; i < goals.length; i++) {
      for (var j = i + 1; j < goals.length; j++) {
        val = $('input[name="' + goals[i].key + '_' + goals[j].key + '"]').val();
        matrix['abs'][i][j] = val;
        matrix['abs'][j][i] = 1/val;
      }
    }
  }

  function normalize_matrix() {
    var col_sums = [];
    for (var j = 0; j < goals.length; j++) {
      col_sums[j] = 0.0;
      for (var i = 0; i < goals.length; i++) {
        col_sums[j] += +matrix['abs'][i][j];
      }
    }

    for (var i = 0; i < goals.length; i++) {
      for (var j = 0; j < goals.length; j++) {
        matrix['norm'][i][j] = matrix['abs'][i][j]/col_sums[j];
      }
    }
  }

  function compute_weights() {
    for (var i = 0; i < goals.length; i++) {
      weights[i] = 0;
      for (var j = 0; j < goals.length; j++) {
        weights[i] += +matrix['norm'][i][j];
      }
	  weights[i] /= +goals.length;
    }
  }

  function compute_consistency_vector() {
    for (var i = 0; i < goals.length; i++) {
      consistency_vector[i] = 0;
      for (var j = 0; j < goals.length; j++) {
        consistency_vector[i] += matrix['abs'][i][j] * weights[j];
      }
	  consistency_vector[i] /= weights[i];
    }
  }
  
  function compute_consistency_ratio() {
	  var lambda = 0;
	  for (var i = 0; i < consistency_vector.length; i++) {
		  lambda += +consistency_vector[i];
	  }
	  lambda /= consistency_vector.length;
	  
	  consistency_index = (lambda - goals.length) / (goals.length - 1);
	  
	  consistency_ratio = consistency_index / random_inconsistency_indices[goals.length];
  }

  function get_matrix() {
var table = $('<table border="1"></table>');

    var headers = $('<tr></tr>');
    table.append(headers);
    headers.append($('<th></th>')); // left column
    for (var i = 0; i < goals.length; i++) {
      headers.append($('<th>' + goals[i].key + '</th>'));
    }

    for (var i = 0; i < goals.length; i++) {
      row = $('<tr></tr>');
      row.append($('<th>' + goals[i].key + '</th>'));
      for (var j = 0; j < goals.length; j++) {
        row.append($('<td>' + matrix['abs'][i][j] +
         ' / <b>' + matrix['norm'][i][j] + '</b></td>'));
      }
      table.append(row);
    }

    row = $('<tr></tr>');
    row.append($('<th>weights</th>'));
    for (var i = 0; i < weights.length; i++) {
      row.append($('<td>' + weights[i] + '</td>'));
    }
    table.append(row);

    row = $('<tr></tr>');
    row.append($('<th>consistency_vectory</th>'));
    for (var i = 0; i < consistency_vector.length; i++) {
      row.append($('<td>' + consistency_vector[i] + '</td>'));
    }
    table.append(row);
	
	row = $('<tr></tr>');
	row.append($('<th>consistency_ratio</th>'));
	row.append($('<td colspan="' + goals.length +'">' + consistency_ratio + '</td>'));
	table.append(row);

    return table;
  }

  function debug() {
   populate_matrix();
   normalize_matrix();
   compute_weights();
   compute_consistency_vector();
   compute_consistency_ratio();
   $('#debug').empty().append(get_matrix());
  }
  
  function validate() {
      populate_matrix();
      normalize_matrix();
      compute_weights();
      compute_consistency_vector();
      compute_consistency_ratio();
	  if (consistency_ratio > 0.1) {
		  alert("Bitte überprüfen Sie Ihre Eingabe");
		  return false;
	  }
  }
  
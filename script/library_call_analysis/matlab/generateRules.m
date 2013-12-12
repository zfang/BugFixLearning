function generateRules(slug)

minus_plus_data = load(strcat(slug, '/minus_plus.txt'));
minus_data = load(strcat(slug, '/minus.txt'));
plus_data = load(strcat(slug, '/plus.txt'));
method_calls = textscan(fopen(strcat(slug, '/method_calls.txt')), '%s');
method_calls = method_calls{1};
method_calls_with_types = textscan(fopen(strcat(slug, '/method_calls_with_types.txt')), '%s');
method_calls_with_types = method_calls_with_types{1};

minSup = .01;
minConf = .5;
nRules = 100;
sortFlag = 1;

fname = strcat(slug, '/minus_plus_result');
findRules(minus_plus_data, minSup, minConf, nRules, sortFlag, method_calls_with_types, fname);

fname = strcat(slug, '/minus_result');
findRules(minus_data, minSup, minConf, nRules, sortFlag, method_calls, fname);

fname = strcat(slug, '/plus_result');
findRules(plus_data, minSup, minConf, nRules, sortFlag, method_calls, fname);

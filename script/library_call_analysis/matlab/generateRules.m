function generateRules(slug)

assoc_minus_plus_data = load(strcat(slug, '/assoc_minus_plus.txt'));
method_calls_with_types = textscan(fopen(strcat(slug, '/method_calls_with_types.txt')), '%s');
method_calls_with_types = method_calls_with_types{1};

assoc_minus_data = load(strcat(slug, '/assoc_minus.txt'));
minus_method_calls = textscan(fopen(strcat(slug, '/method_calls_minus.txt')), '%s');
minus_method_calls = minus_method_calls{1};

assoc_plus_data = load(strcat(slug, '/assoc_plus.txt'));
plus_method_calls = textscan(fopen(strcat(slug, '/method_calls_plus.txt')), '%s');
plus_method_calls = plus_method_calls{1};

minSup = .01;
minConf = .5;
nRules = 100;
sortFlag = 1;

fname = strcat(slug, '/assoc_minus_plus_result');
findRules(assoc_minus_plus_data, minSup, minConf, nRules, sortFlag, method_calls_with_types, fname);

fname = strcat(slug, '/assoc_minus_result');
findRules(assoc_minus_data, minSup, minConf, nRules, sortFlag, minus_method_calls, fname);

fname = strcat(slug, '/assoc_plus_result');
findRules(assoc_plus_data, minSup, minConf, nRules, sortFlag, plus_method_calls, fname);

tfidf_minus_data = load(strcat(slug, '/tfidf_minus.txt'));
tfidf_plus_data = load(strcat(slug, '/tfidf_plus.txt'));
%TODO

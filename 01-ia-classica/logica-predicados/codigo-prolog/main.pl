avaliaAborto:- write('quantos abortos a gestante teve? '),
		read(Aborto),
		(abortos(Aborto);true),!.

avaliaIdGest:- write('qual a idade da gestante? '),
		read(Idade),
		write('quantos partos a gestante ja passou? '),
		read(Partos),
		(defineIdadeNumFilhos(Idade,Partos);true),!.

avaliaPreNatal:- write('a gestante fez pre natal? '),
		read(Natal),
		(preNatal(Natal);true),!.

avaliaDiabete:- write('a gestante possui diabetes? '),
		read(Diabetes),
		(diabetes(Diabetes);true),!.

avaliaHipertensao:- write('a gestante possui hipertensao? '),
		read(Hipertensao),
		(hipertensao(Hipertensao);true),!.

avaliaPlacenta:- write('houve descolamento prematuro da placenta da gestante? '),
		read(Placenta),
		(deslocamentoPlacenta(Placenta);true),!.

avaliaHemo:- write('a gestante possui hemofilia? '),
		read(Hemofilia),
		(hemofilia(Hemofilia);true),!.

avaliaAnemia:- write('a gestante possui anemia falciforme? '),
		read(Anemia),
		(anemiaFalciforme(Anemia);true),!.

avaliaChagas:- write('a gestante possui doenca de chagas? '),
		read(Chagas),
		(doencaChagas(Chagas);true),!.

avaliaDst:- write('a gestante possui dst? '),
		read(Dst),
		(dst(Dst);true),!.

avaliaNeuro:- 	write('a gestante possui neurocistecercose? '),
		read(Neuro),
		(neurocistecercose(Neuro);true),!.

avaliaIctericia:- write('a gestante possui tipo sanguineo incompativel com a do bebe (icteceria grave)? '),
		read(Icteceria),
		(ictericia(Icteceria);true),!.

avaliaRubeola:- write('a gestante tem ou teve rubeola ao longo da gestante? '),
		read(Gestante),
		(rubeola(Gestante);true),!.

avaliaObesa:- write('a gestante eh obesa? '),
		read(Obesa),
		(obesidade(Obesa);true),!.

avaliaAlcool:- write('a gestante faz uso de alcool ou tabaco? '),
		read(Alcool),
		(alcoolTabaco(Alcool);true),!.

avaliaDroga:- write('a gestante eh usuaria de drogas? '),
		read(Drogas),
		(drogas(Drogas);true),!.

avaliaCardio:- write('a gestante possui cardiopatia? '),
		read(Cardio),
		(cardiopatia(Cardio);true),!.

avaliaFisico:- 	write('continuar com a gestaçao poderia causar problemas fisicos a gestante? '),
		read(Fisico),
		(defineProbFisicos(Fisico);true),!.

avaliaMental:- 	write('continuar com a gestaçao poderia causar problemas mentais a gestante? '),
		read(Mental),
		(defineProbMentais(Mental);true),!.

avaliaEstupro:- write('a gestante foi vitima de estupro? '),
		read(Est),
		(defineEstupro(Est);true),!.

avaliaAnencefalia:- write('o bebe tem anencefalia? '),
		read(Anencefalia),
		(defineAnencefalia(Anencefalia);true),!.

avaliaMoradia :- write('a gestante mora sozinha? '),
		read(Mora),
		(moraSozinha(Mora);true),!.

avaliaDepressao:- write('a gestante tem depressao? '),
		read(Depre),
		(depressao(Depre);true),!.

avaliaCompanheiro:- write('a gestante tem um companheiro? '),
		read(Comp),
		(temCompanheiro(Comp);true),!.

avaliaGravidez:- write('a gravidez foi desejada? '),
		read(Desejada),
		(gravidezDesejada(Desejada);true),!.

avaliaDependente:- write('a gestante eh dependente quimica? '),
		read(Dependente),
		(dependenteQuimica(Dependente);true),!.

avaliaEstuprada:- write('a gestante foi estuprada? '),
		read(Est),
		(foiEstuprada(Est);true),!.


avaliaRisco:-	avaliaAborto,
		avaliaIdGest,
		avaliaPreNatal,
		avaliaDiabete,
		avaliaHipertensao,
		avaliaPlacenta,
		avaliaHemo,
		avaliaAnemia,
		avaliaChagas,
		avaliaDst,
		avaliaNeuro,
		avaliaIctericia,
		avaliaRubeola,
		avaliaObesa,
		avaliaAlcool,
		avaliaDroga,
		avaliaCardio,
		avaliaFisico,
		avaliaMental,
		avaliaEstupro,
		avaliaAnencefalia,!.

avaliaPsico:- avaliaMoradia,
		avaliaDepressao,
		avaliaCompanheiro,
		avaliaGravidez,
		avaliaDependente,
		avaliaEstuprada,!.

avaliaSocio:- write('Quantos salarios minimos a gestante recebe? '),
		read(Salario),
		write('Quantos individuos invalidos ou sustentados na casa? '),
		read(Ind),
		(defineRendaInvalidos(Salario,Ind);true),!.

printRisco:- defineNivelRisco,definePassivelAborto,
	nivelRisco(Risco),
	write('o nivel de risco eh '),write(Risco),nl,
	passivelAborto(Aborto),
	write('eh passivel de aborto? '),write(Aborto),nl,
	risco(R),Percent is R*100,
	write('grau de certeza de que ha risco: '),write(Percent),write('%'),nl,!.

printPsico:- assistPsico(Psi),
	write('eh preciso acompanhamento psicologico? '),write(Psi),nl,!.

printSocio:- assistSocial(Soc),
	write('eh preciso de acompanhamento social? '),write(Soc),nl,!.

main:- consult('avaliaRisco.pl'),
	consult('avaliaPsico.pl'),
	consult('avaliaSocial.pl'),
	avaliaRisco,printRisco,
	avaliaPsico,printPsico,
	avaliaSocio,printSocio,
	!.


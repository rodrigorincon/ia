avaliaAborto:- (abortos(0);true),!.

avaliaIdGest:- (defineIdadeNumFilhos(23,0);true),!.

avaliaPreNatal:- (preNatal(true);true),!.

avaliaDiabete:- (diabetes(false);true),!.

avaliaHipertensao:- (hipertensao(true);true),!.

avaliaPlacenta:- (deslocamentoPlacenta(true);true),!.

avaliaHemo:- (hemofilia(false);true),!.

avaliaAnemia:- (anemiaFalciforme(true);true),!.

avaliaChagas:- (doencaChagas(false);true),!.

avaliaDst:- (dst(false);true),!.

avaliaNeuro:- (neurocistecercose(false);true),!.

avaliaIctericia:- (ictericia(true);true),!.

avaliaRubeola:- (rubeola(false);true),!.

avaliaObesa:- (obesidade(true);true),!.

avaliaAlcool:- (alcoolTabaco(false);true),!.

avaliaDroga:- (drogas(true);true),!.

avaliaCardio:- (cardiopatia(true);true),!.

avaliaFisico:- (defineProbFisicos(false);true),!.

avaliaMental:- (defineProbMentais(false);true),!.

avaliaEstupro:- (defineEstupro(true);true),!.

avaliaAnencefalia:- (defineAnencefalia(false);true),!.

avaliaMoradia :- (moraSozinha(false);true),!.

avaliaDepressao:- (depressao(false);true),!.

avaliaCompanheiro:- (temCompanheiro(true);true),!.

avaliaGravidez:- (gravidezDesejada(true);true),!.

avaliaDependente:- (dependenteQuimica(false);true),!.

avaliaEstuprada:- (foiEstuprada(true);true),!.


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

avaliaSocio:- defineRendaInvalidos(2,6),!.

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


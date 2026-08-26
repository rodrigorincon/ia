%--------------------------VARIAVEIS OBJETIVO----------------------

:- dynamic riscoPara/2.
riscoPara(bebe,false).
riscoPara(ambos,false).

%regras que controlam os fatos sobre riscoPara
riscoBebe :- riscoPara(bebe,false),retract(riscoPara(bebe,_)), assert(riscoPara(bebe,true)),!.
riscoAmbos :- riscoPara(ambos,false),retract(riscoPara(ambos,_)), assert(riscoPara(ambos,true)),!.

:- dynamic risco/1.
risco(0). 

%regra que controla o valor sobre de risco
calcRisco(Num) :- risco(Antigo),retract(risco(_)),Novo is Antigo+Num-(Antigo*Num),assert(risco(Novo)),!.

:- dynamic nivelRisco/1.
%nivelRisco(baixo). nivelRisco(moderado). nivelRisco(alto). nivelRisco(vida).
%ñ cria nenhum fato inicialmente, cria após responder as perguntas e ter o valor de risco definido

%regra que define o nivel do risco de vida dos envolvidos
defineNivelRisco :- risco(R), R =< 0.3 -> assert(nivelRisco(leve));
		risco(R), R > 0.3, R =< 0.65 -> assert(nivelRisco(moderado));
		risco(R), R > 0.65, R =< 0.9 -> assert(nivelRisco(alto));
		risco(R), R > 0.9 -> assert(nivelRisco(vida));!.

:- dynamic passivelAborto/1.
%passivelAborto(true). passivelAborto(false).

definePassivelAborto :- nivelRisco(vida), riscoPara(ambos,true) -> assert(passivelAborto(true));
			probFisicos(true) -> assert(passivelAborto(true));
			probMentais(true) -> assert(passivelAborto(true));
			estupro(true) -> assert(passivelAborto(true));
			anencefalia(true) -> assert(passivelAborto(true));
			not(nivelRisco(vida)),not(anencefalia(true)),not(probFisicos(true)),not(probMentais(true)),not(estupro(true)) -> assert(passivelAborto(false));!.

%----------------------VARIAVEIS PARA DEFINIR O VALOR DO NÍVEL----------------------

%regras que avaliam o risco a partir da idade e numero de filhos
defineIdadeNumFilhos(I,F) :- I =< 16 -> calcRisco(0.66), riscoAmbos;
			I > 40 -> calcRisco(0.68), riscoAmbos;
			I > 16, I =< 35 -> calcRisco(0.05);
			I > 35, I =< 40, F>4 -> calcRisco(0.66), riscoAmbos;
			I > 35, I =< 40, F=<4 -> calcRisco(0.35), riscoAmbos;!.

abortos(Num) :- (Num == 1 ; Num == 2 ) -> riscoBebe, calcRisco(0.50);
		Num > 2 -> riscoBebe, calcRisco(0.67);!.

preNatal(SimNao) :- not(SimNao), calcRisco(0.31), riscoAmbos,!.
diabetes(SimNao) :- SimNao, calcRisco(0.75), riscoAmbos,!.
hipertensao(SimNao) :- SimNao, calcRisco(0.75), riscoAmbos,!.
deslocamentoPlacenta(SimNao) :- SimNao, calcRisco(0.71), riscoAmbos,!.
hemofilia(SimNao) :- SimNao, calcRisco(0.90), riscoAmbos,!.
anemiaFalciforme(SimNao) :- SimNao, calcRisco(0.90), riscoAmbos,!.
doencaChagas(SimNao) :- SimNao, calcRisco(0.70), riscoAmbos,!.
dst(SimNao) :- SimNao, calcRisco(0.70), riscoBebe,!.
neurocistecercose(SimNao) :- SimNao, calcRisco(0.70), riscoBebe,!.
ictericia(SimNao) :- SimNao, calcRisco(0.67), riscoBebe,!.
rubeola(SimNao) :- SimNao, calcRisco(0.69), riscoBebe,!.
obesidade(SimNao) :- SimNao, calcRisco(0.80), riscoAmbos,!.
alcoolTabaco(SimNao) :- SimNao, calcRisco(0.70), riscoBebe,!.
drogas(SimNao) :- SimNao, calcRisco(0.75), riscoBebe,!.
cardiopatia(SimNao) :- SimNao, calcRisco(0.70), riscoAmbos,!.

%----------------------VARIAVEIS PARA DEFINIR O NIVEL DO RISCO----------------------

:- dynamic probFisicos/1.
probFisicos(false).
defineProbFisicos(SimNao) :- SimNao, retract(probFisicos(_)), assert(probFisicos(true)).

:- dynamic estupro/1.
estupro(false).
defineEstupro(SimNao) :- SimNao, retract(estupro(_)), assert(estupro(true)).

:- dynamic anencefalia/1.
anencefalia(false).
defineAnencefalia(SimNao) :- SimNao, retract(anencefalia(_)), assert(anencefalia(true)).

:- dynamic probMentais/1.
probMentais(false).
defineProbMentais(SimNao) :- SimNao, retract(probMentais(_)), assert(probMentais(true)).

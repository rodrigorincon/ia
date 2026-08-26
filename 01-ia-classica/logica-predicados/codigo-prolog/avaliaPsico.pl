:- dynamic assistPsico/1.
assistPsico(false).

moraSozinha(SimNao) :- SimNao, retract(assistPsico(_)), assert(assistPsico(true)),!.
depressao(SimNao) :- SimNao, retract(assistPsico(_)), assert(assistPsico(true)),!.
temCompanheiro(SimNao) :- not(SimNao), retract(assistPsico(_)), assert(assistPsico(true)),!.
gravidezDesejada(SimNao) :- not(SimNao), retract(assistPsico(_)), assert(assistPsico(true)),!.
dependenteQuimica(SimNao) :- SimNao, retract(assistPsico(_)), assert(assistPsico(true)),!.
foiEstuprada(SimNao) :- SimNao, retract(assistPsico(_)), assert(assistPsico(true)),!.

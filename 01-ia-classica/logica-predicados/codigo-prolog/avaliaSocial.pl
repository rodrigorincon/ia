:- dynamic assistSocial/1.
assistSocial(false). 

defineRendaInvalidos(Renda,Inv) :- Renda == 0 -> retract(assistSocial(_)), assert(assistSocial(true));
				Renda >=1, Renda =< 3, Inv>=5 -> retract(assistSocial(_)), assert(assistSocial(true));
				Renda == 4, Inv > 7 -> retract(assistSocial(_)), assert(assistSocial(true));!.

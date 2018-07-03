/**
 * Clauses are represented by assigning distinct positive 
 * non-zero integers to propositional variables:
 *    x1 v .. v xn --> [x1, .. , xn]
 *    ~x           --> -x
 *
 * DPLL algorithm variant used to check satisfiability.
 */

% mem(+Elem, +List)
mem(X, [X|_]).
mem(X, [_|Y]) :-
   mem(X, Y).

% sel(+Elem, +List, -List)
sel(X, [X|Y], Y).
sel(X, [Y|Z], [Y|T]) :-
   sel(X, Z, T).

% filter(+ListOfList, +Elem, +Elem, -ListOfList)
filter([], _, _, []).
filter([K|F], L, M, [J|G]) :-
   sel(M, K, J), !,
   J \== [],
   filter(F, L, M, G).
filter([K|F], L, M, G) :-
   mem(L, K), !,
   filter(F, L, M, G).
filter([K|F], L, M, [K|G]) :-
   filter(F, L, M, G).

% sat(+ListOfLists, -List)
sat([[L|_]|F], [L|V]):-
   M is -L,
   filter(F, L, M, G),
   sat(G, V).
sat([[L|K]|F], [M|V]):-
   K \== [],
   M is -L,
   filter(F, M, L, G),
   sat([K|G], V).
sat([], []).

% ?- sat([[1,-2],[-1,-2],[1,3]], X).
% X = [1,-2] ;
% X = [-1,-2,3] ;
% No

% Pigeon Hole Problem 2x2
% ?- sat([[11, 12],[21, 22],[-11, -21],[-12, -22]], X).
% X = [11,-21,22,-12] ;
% X = [-11,12,21,-22] ;
% No
 
% Pigeon Hole Problem 3x2
% ?- sat([[11, 12],[21, 22],[31, 32],[-11, -21],[-11, -31],
% [-21, -31],[-12, -22],[-12, -32], [-22, -32]], X).
% No
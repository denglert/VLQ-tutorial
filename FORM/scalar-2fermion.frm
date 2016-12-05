Vectors p1, p2, s1, s2;
Symbols m1, m2;

Local M2 =
1/4 *
(
(g_(1,p1) + m1) *
(gi_(1) + g5_(1)*g_(1,s1) ) *
(g_(1,p2) - m2) *
(gi_(1) + g5_(1)*g_(1,s2) )
)
;

Trace4,1;

id p1.s1 = 0;
id p2.s2 = 0;

Bracket p1.p2;

Print;
.sort

.end

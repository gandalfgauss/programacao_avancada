//Disponível em: https://github.com/morris821028/UVa/blob/master/volume101/10117%20-%20Nice%20Milk.cpp

/*
O problema:
    Contem entradas n, k, h
    Onde n eh o numero de pontos que o poligono convexo tera (o pao eh esse poligono)
    Esse pao tem que ser molhado no copo de leite de altura h no copo
    E k eh o numero de acoes que devem ser feitas no intuito de maximar a area molhada de leite no pao
    O problema deve retornar a area molhada que foi maximizada ao executar k acoes de molhar o pao(poligono convexo)
    em um copo de leite, com altura h de leite no copo.
*/

/*
Este código implementa o algoritmo de interseção de meio-plano, que é usado para calcular a interseção
de um conjunto de meio-planos (ou seja, regiões delimitadas por linhas infinitas).

O código começa definindo uma estrutura de ponto (Pt) que armazena as coordenadas de um ponto em um plano bidimensional.

Em seguida, há funções auxiliares para calcular o produto interno (dot) e o produto vetorial (cross) entre vetores.

Há também uma função para verificar se um ponto (c) está entre dois outros pontos (a e b)
e outra função para verificar se um ponto (c) está em uma reta que passa por dois outros pontos (a e b).

Em seguida, há uma estrutura de segmento (Seg), que é definida por dois pontos (s e e)
e um ângulo que é calculado a partir desses pontos usando a função atan2.
Essa estrutura também tem um rótulo (label) para identificar cada segmento.

A seguir, há uma função getIntersect que calcula a interseção entre dois segmentos (a e b).
Isso é feito usando o produto vetorial para encontrar o ponto em que as duas linhas infinitas se cruzam e, em seguida,
o parâmetro t é calculado para determinar a posição desse ponto na linha que liga os dois pontos de cada segmento.

A função halfPlaneIntersect é a principal função deste código e é usada para calcular a interseção
de um conjunto de meio-planos. Isso é feito da seguinte maneira:

- Os segmentos são ordenados pelo ângulo que fazem com o eixo x, usando a função sort.
- Os segmentos com o mesmo ângulo são agrupados, removendo os duplicados(set).
- Uma fila(deq) de segmentos é usada para manter os segmentos que definem a região de interseção atual.
- Os segmentos são adicionados um a um à fila, removendo os segmentos que não fazem mais parte da região de interseção
  à medida que novos segmentos são adicionados.
- A interseção dos segmentos restantes é calculada e retornada como um vetor de pontos.
- Finalmente, há uma função calcArea que calcula a área de um polígono representado como um vetor de pontos.
  Isso é feito usando a fórmula de Shoelace, que consiste em somar as áreas dos trapézios
  formados pelos pares de pontos consecutivos do polígono.

  O restante do código é apenas uma implementação do algoritmo para resolver um problema específico:
  dado um conjunto de pontos (n)(pontos) que representam as bordas de uma região(pão) e uma altura (h),
  encontrar a área da interseção da região(pão) com um plano horizontal a uma distância h acima do plano
  que contém os pontos.

*/
#include <stdio.h>
#include <math.h>
#include <algorithm>
#include <set>
#include <vector>
using namespace std;

#define eps 1e-10
#define MAXN 131072
struct Pt {
    double x, y;
    Pt(double a = 0, double b = 0):
    	x(a), y(b) {}
	Pt operator-(const Pt &a) const {
        return Pt(x - a.x, y - a.y);
    }
    Pt operator+(const Pt &a) const {
        return Pt(x + a.x, y + a.y);
    }
    Pt operator*(const double a) const {
        return Pt(x * a, y * a);
    }
    bool operator<(const Pt &a) const {
		if (fabs(x - a.x) > eps)
			return x < a.x;
		if (fabs(y - a.y) > eps)
			return y < a.y;
		return false;
	}
};
double dot(Pt a, Pt b) {
	return a.x * b.x + a.y * b.y;
}
double cross(Pt o, Pt a, Pt b) {
    return (a.x-o.x)*(b.y-o.y)-(a.y-o.y)*(b.x-o.x);
}
double cross2(Pt a, Pt b) {
    return a.x * b.y - a.y * b.x;
}
int between(Pt a, Pt b, Pt c) {
	return dot(c - a, b - a) >= -eps && dot(c - b, a - b) >= -eps;
}
int onSeg(Pt a, Pt b, Pt c) {
	return between(a, b, c) && fabs(cross(a, b, c)) < eps;
}
struct Seg {
	Pt s, e;
	double angle;
	int label;
	Seg(Pt a = Pt(), Pt b = Pt(), int l=0):s(a), e(b), label(l) {
		angle = atan2(e.y - s.y, e.x - s.x);
	}
	bool operator<(const Seg &other) const {
		if (fabs(angle - other.angle) > eps)
			return angle > other.angle;
		if (cross(other.s, other.e, s) > -eps)
			return true;
		return false;
	}
};
Pt getIntersect(Seg a, Seg b) {
	Pt u = a.s - b.s;
    double t = cross2(b.e - b.s, u)/cross2(a.e - a.s, b.e - b.s);
    return a.s + (a.e - a.s) * t;
}
Seg deq[MAXN];
vector<Pt> halfPlaneIntersect(vector<Seg> segs) {
	sort(segs.begin(), segs.end());
	int n = segs.size(), m = 1;
	int front = 0, rear = -1;
	for (int i = 1; i < n; i++) {
		if (fabs(segs[i].angle - segs[m-1].angle) > eps)
			segs[m++] = segs[i];
	}
	n = m;
	deq[++rear] = segs[0];
	deq[++rear] = segs[1];
	for (int i = 2; i < n; i++) {
		while (front < rear && cross(segs[i].s, segs[i].e, getIntersect(deq[rear], deq[rear-1])) < eps)
			rear--;
		while (front < rear && cross(segs[i].s, segs[i].e, getIntersect(deq[front], deq[front+1])) < eps)
			front++;
		deq[++rear] = segs[i];
	}
	while (front < rear && cross(deq[front].s, deq[front].e, getIntersect(deq[rear], deq[rear-1])) < eps)
		rear--;
    while (front < rear && cross(deq[rear].s, deq[rear].e, getIntersect(deq[front], deq[front+1])) < eps)
    	front++;
    vector<Pt> ret;
	for (int i = front; i < rear; i++) {
		Pt p = getIntersect(deq[i], deq[i+1]);
		ret.push_back(p);
	}
	if (rear > front + 1) {
		Pt p = getIntersect(deq[front], deq[rear]);
		ret.push_back(p);
	}
	return ret;
}
double calcArea(vector<Pt> p) {
	double ret = 0;
	int n = p.size();
	if(n < 3) return 0.0;
	for(int i = 0, j = n-1; i < n; j = i++)
		ret += p[i].x * p[j].y - p[i].y * p[j].x;
	return fabs(ret)/2;
}
Pt D[32];
int main() {
	int n, m;
	double h;
	while (scanf("%d %d %lf", &n, &m, &h) == 3 && n) {
		vector<Pt> O;
		Seg Oe[32];
		for (int i = 0; i < n; i++) {
			scanf("%lf %lf", &D[i].x, &D[i].y);
			O.push_back(D[i]);
		}
		D[n] = D[0], O.push_back(D[0]);
		for (int i = 0; i < n; i++) {
			Pt a = D[i], b = D[i+1]; // \vec{ab}
			Pt nab(b.y - a.y, a.x - b.x); // normal vector
			double v = hypot(nab.x, nab.y);
			nab.x = nab.x / v * h, nab.y = nab.y / v * h;
			a = a - nab, b = b - nab;
			Oe[i] = Seg(a, b);
		}
		int A[32] = {};
		for (int i = 0; i < m; i++)
			A[i] = 1;
		sort(A, A+n);
		double area = calcArea(O), ret = 0;
		do {
			vector<Seg> segs;
			for (int i = 0; i < n; i++)
				if (A[i])
					segs.push_back(Oe[i]);
				else
					segs.push_back(Seg(O[i], O[i+1]));
			vector<Pt> convex = halfPlaneIntersect(segs);
			double d = calcArea(convex);
			ret = max(ret, area - d);
		} while (next_permutation(A, A+n));
		printf("%.2lf\n", ret);
	}
	return 0;
}

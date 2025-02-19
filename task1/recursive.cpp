#include <iostream>
#include <vector>
#include <string>

//////////////////////////////////////////////////////////////////////
//                                                                  //
//  Push: Inserta un elemento en la pila.                           //
//  Pop: Elimina el elemento en la parte superior de la pila.       //
//  Top: Devuelve el elemento en la parte superior sin eliminarlo.  //
//  Empty: Comprueba si la pila está vacía.                         //
//  Size: Devuelve el número de elementos en la pila.               //
//                                                                  //
//////////////////////////////////////////////////////////////////////

using namespace std;

class Tower {
    char name;
    vector<int> disks;

public:
    Tower(char n) : name(n) {}

    void add_disk(int disk) {
        disks.push_back(disk);
    }

    int peek() const {
        return disks.empty() ? -1 : disks.back();
    }

    bool remove_top() {
        if (disks.empty()) return false;
        disks.pop_back();
        return true;
    }

    bool empty() const {
        return disks.empty();
    }

    char getName() const {
        return name;
    }

    friend ostream& operator<<(ostream& os, const Tower& t) {
        os << t.name << "=(";
        for (size_t i = 0; i < t.disks.size(); ++i) {
            if (i > 0) os << ",";
            os << t.disks[i];
        }
        os << ")";
        return os;
    }
};

void move_disks(int n, Tower& source, Tower& destination, Tower& auxiliary, int& move_count) {
    if (n == 1) {
        int disk = source.peek();
        source.remove_top();
        destination.add_disk(disk);
        ++move_count;
        cout << move_count << ". Move disk " << disk 
             << " from " << source.getName() << " to " << destination.getName() 
             << ". " << source << ", " << auxiliary << ", " << destination << ".\n";
        return;
    }

    //para n-1
    move_disks(n - 1, source, auxiliary, destination, move_count);

    //para el disco mas grande
    move_disks(1, source, destination, auxiliary, move_count);

    //para n-1 que queda en la torre auxiliar
    move_disks(n - 1, auxiliary, destination, source, move_count);
}

void solve_hanoi(int n) {
    if (n < 1 || n > 10) {
        cout << "Error: n must be between 1 and 10\n";
        return;
    }

    cout << "n = " << n << "\n";

    Tower a('A'), b('B'), c('C');
    for (int i = n; i >= 1; --i) {
        a.add_disk(i);
    }

    cout << "Initial state: " << a << ", " << b << ", " << c << ".\n";

    int move_count = 0;
    move_disks(n, a, c, b, move_count);
}

int main() {
    int n;
    cout << "Enter number of disks (1-10): ";
    cin >> n;
    solve_hanoi(n);
    return 0;
}

/*
Self Notes:

	1. Primero tenemos la clase que tiene dos atributos, nombre y un vector de enteros que representan los discos que se apilan en la torre, es decir cada instancia de esta clase tendra un nombre diferente (A, B, C) y un numero de discos que puede ser 0, 1, 2 o 3.
	
	2. La clase tiene un constructor que la inicializa con un nombre (A, B, C).
	 
	3. El primer metodo pushea en una torre especifica a la que se le aplique el metodo un disco en modo de pila con la funcion push back.
	
	4. El segundo metodo llamado peek retorna el numero del disco en la parte superior pero no lo quita, it's literally taking a peek at it. Si la torre está vacía va a devolver -1.
	
	5. El tercer metodo de la clase remove_top(), Si hay discos, elimina el disco superior y devuelve true, Lo saca mediante la funcion de la pila pop_back. Y si la torre esta vacia devuelve false.
	
	6. El cuarto metodo llamado empty solo se asegura de que la torre esta vacia, es un bool asi que en tal caso devolverá true.
	
	7. El quinto metodo es un getter, devuelve el nombre de la torre al que se le aplica.
	
	8. Luego printeamos el estado de la torre con nombre y discos en el formato que se nos pide. Se usa sobrecarga del operador << para ostream.
	
	9. Tenemos luego la funcion move_disks qur consta de los siguientes parametros:
		n: numero de discos a mover
		source: torre origen
		destination: torre destino
		auxiliary: torre auxiliar (la del medio)
		move_count: contador de movimientos
		
	10. Tenemos un caso base que es cuando hay un disco solo, es decir n == 1. Si hay solo un solo disco, se mueve directamente de source a destination. Se incrementa move_count y se imprime el estado actual.
	
	11. Si es recursivo, hay tres pasos y llamamos a la misma funcion dentro de ella, primero mueve n-1 discos de source a auxiliary, usando destination como auxiliar, mueve el disco más grande de source a destination, mueve los n-1 discos de auxiliary a destination, usando source como auxiliar.

	12. La funcion de error. Si n no esta en el rango correcto, devuelve error.
	
	13. La funcion que inicia las torres. Crea las torres A, B y C y llena la A con n discos.
	
	14. La resolucion del problema empieza mostrando el estado inicial de las torres y llama luego a move_disks para empezar a resolver. Pero antes de llamar a la funcion inicializa el move_count a 0.

*/
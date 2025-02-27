#include <iostream>
#include <vector>
#include <iomanip>
using namespace std;

const int N = 5;
const int NN = N * N;
int board[N][N] = {0};
int cx[8] = {2, 1, -1, -2, -2, -1, 1, 2};
int cy[8] = {1, 2, 2, 1, -1, -2, -2, -1};
long long trials = 0;

void printBoard() {
    cout << "\n2) Path graphically:" << endl;
    cout<< endl;
    cout << "Y, V ^" << endl;

    for (int i = N - 1; i >= 0; --i) {
        cout << i + 1 << " | ";
        for (int j = 0; j < N; ++j) {
            cout << setw(2) << board[j][i] << " ";
        }
        cout << endl;
    }
    cout << "  -------------------> X, U\n    1  2  3  4  5\n";
}

void tryMove(int l, int x, int y, bool &found, string trace = "") {
    trials++;
    for (int k = 0; k < 8; k++) {
        int u = x + cx[k], v = y + cy[k];
        if (u >= 0 && u < N && v >= 0 && v < N && board[u][v] == 0) {
            board[u][v] = l;
            cout << trials << ") " << trace << "R" << (k + 1) << ". U=" << (u + 1) << ", V=" << (v + 1) << ". L=" << l;
            if (l < NN) { 
                cout << ". Free. BOARD[" << (u + 1) << ", " << (v + 1) << "]=" << l << "." << endl;
                tryMove(l + 1, u, v, found, trace + "-");
                if (!found) {
                    board[u][v] = 0;
                    cout << trace << "Backtrack." << endl;
                }
            } else {
                cout << ". Path found!" << endl;
                found = true;
                return;
            }
        } else {
            cout << trials << ") " << trace << "R" << (k + 1) << ". U=" << (u + 1) << ", V=" << (v + 1) << ". L=" << l << ". Out." << endl;
        }
        if (found) return;
    }
}

int main() {
    cout << "PART 1. Data" << endl;
    cout << "1) Board: 5x5." << endl;
    cout << "2) Initial position: X=1, Y=1. L=1." << endl;
    
    bool found = false;
    board[0][0] = 1;
    tryMove(2, 0, 0, found);
    
    cout << "\nPART 3. Results" << endl;
    if (found) {
        cout << "1) Path is found. Trials=" << trials << ".";
        printBoard();
    } else {
        cout << "Path does not exist." << endl;
    }
    return 0;
}

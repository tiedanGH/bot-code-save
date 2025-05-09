#include <vector>
#include <iostream>
using namespace std;

const int k_map_size = 73;
const int maps[1][k_map_size] = {
    // 经典
    {
        1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 0, 0, 0, 1, 1, 1,
        1, 1, 0, 0, 0, 0, 1, 1,
        1, 1, 0, 0, 0, 0, 0, 1, 1,
        1, 1, 0, 0, 0, 0, 1, 1,
        1, 1, 1, 0, 0, 0, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1,
    }
};

vector<int> numToid;

void analysisMap() {
    int empty = 0;
    for (int i = 0; i < k_map_size; i++) {
        if (maps[0][i] == 1) {
            numToid.push_back(i);
        } else {
            numToid.insert(numToid.begin() + empty, i);
            empty++;
        }
    }
}

int main() {
	analysisMap();
    for (int i = 0; i < k_map_size; i++) {
        cout << numToid[i] << " ";
    }
}
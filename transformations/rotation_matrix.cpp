#include "ioh.hpp"

using namespace std;
using namespace ioh;

std::vector<std::vector<double>> compute_rotation(const long rotation_seed,
                                                  const int n_variables)
{
    const auto random_vector = common::random::bbob2009::normal(
        static_cast<size_t>(n_variables) * n_variables, rotation_seed);
    auto matrix = std::vector<std::vector<double>>(
        n_variables, std::vector<double>(n_variables));

    // reshape
    for (auto i = 0; i < n_variables; i++)
        for (auto j = 0; j < n_variables; j++)
            matrix[i][j] =
                random_vector.at(static_cast<size_t>(j) * n_variables + i);


    /*1st coordinate is row, 2nd is column.*/
    for (long i = 0; i < n_variables; i++)
    {
        for (long j = 0; j < i; j++)
        {
            auto prod = 0.0;
            for (auto k = 0; k < n_variables; k++)
                prod += matrix[k][i] * matrix[k][j];

            for (auto k = 0; k < n_variables; k++)
                matrix[k][i] -= prod * matrix[k][j];
        }
        auto prod = 0.0;
        for (auto k = 0; k < n_variables; k++)
            prod += matrix[k][i] * matrix[k][i];

        for (auto k = 0; k < n_variables; k++)
            matrix[k][i] /= sqrt(prod);
    }
    return matrix;
}

void writ_matrx(std::vector<std::vector<double>> matrix, string file_path)
{
    ofstream fout;
    fout.open(file_path, ios::out);
    for (auto line : matrix)
    {
        for (auto num : line)
            fout << num << " ";
        fout << endl;
    }
    fout.close();
}

int main()
{
    std::vector<std::vector<double>> matrix;
    for (int i = 0; i < 30; i++)
    {
        long seed = rand();
        matrix = compute_rotation(seed, 10);
        stringstream ss;
        ss << "results/rotation_matrix/" << i << "_rotation_10.txt";
        writ_matrx(matrix, ss.str());
    }
}
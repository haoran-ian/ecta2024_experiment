#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <iterator>
#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

// Define a type for convenience
using Matrix = std::vector<std::vector<double>>;
using ThreeDimVector = std::vector<Matrix>;

const int num_sampling = 100;
const int num_x = 1000;
const int dim = 10;

void read_x(vector<vector<vector<double>>> &x_sets)
{
    stringstream ss;
    ss << setw(3) << setfill('0') << dim;
    string dim_str = ss.str();
    ifstream fin;
    fin.open("config/samplingX_" + dim_str + "D.txt", ios::in);
    double read_cache;
    string header;
    for (int i = 0; i < num_sampling; i++)
    {
        for (int j = 0; j < dim; j++)
            fin >> header;
        vector<vector<double>> x;
        for (int j = 0; j < num_x; j++)
        {
            fin >> header;
            vector<double> x_cache;
            for (int k = 0; k < dim; k++)
            {
                fin >> read_cache;
                x_cache.push_back(read_cache);
            }
            x.push_back(x_cache);
        }
        x_sets.push_back(x);
    }
    fin.close();
}

// Function to read matrices into a 3D vector
ThreeDimVector read_matrices_to_array(const std::string &filename)
{
    std::ifstream file(filename);
    ThreeDimVector matrices;
    std::string line;
    if (!file.is_open())
    {
        std::cerr << "Error opening file." << std::endl;
        return matrices;
    }
    int num_matrices = 0;
    Matrix current_matrix;
    int count = 0;
    while (std::getline(file, line) && num_matrices < 100)
    {
        if (line[0] == '#' || line[0] == 'B' || line.size() < 10)
            continue;
        std::istringstream iss(line);
        std::vector<double> row(std::istream_iterator<double>{iss},
                                std::istream_iterator<double>());
        if (row.size() == 10)
        {
            current_matrix.push_back(row);
            if (current_matrix.size() == 10)
            {
                matrices.push_back(current_matrix);
                current_matrix.clear();
                num_matrices++;
            }
        }
    }
    file.close();
    return matrices;
}

int main()
{
    std::string filename = "config/random_look_10d_rotation_matrices.txt";
    ThreeDimVector matrices = read_matrices_to_array(filename);
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);
    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        const auto &problem_factory =
            ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
        auto problem = problem_factory.create(problem_id, 1, dim);
        for (int i = 0; i < matrices.size(); i++)
        {
            Matrix rotation_matrix(matrices[i]);
            std::string filename = "ecta2024_data/x_rotation/" +
                                   std::to_string(problem_id) + "_" +
                                   std::to_string(i) + ".txt";
            std::ofstream file(filename);
            for (int j = 0; j < num_sampling; j++)
            {
                for (int k = 0; k < num_x; k++)
                {
                    vector<double> x(x_sets[j][k]);
                    vector<double> cacheX(x);
                    for (int m = 0; m < dim; m++)
                    {
                        x.at(m) = 0;
                        for (int n = 0; n < dim; n++)
                        {
                            x.at(m) = x.at(m) +
                                      cacheX.at(n) * rotation_matrix[m][n];
                        }
                    }
                    file << (*problem)(x) << " ";
                }
                file << endl;
            }
            file.close();
        }
    }
    return 0;
}

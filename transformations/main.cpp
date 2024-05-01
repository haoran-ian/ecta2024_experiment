#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

const int num_sampling = 100;
const int num_x = 1000;
const int dim = 2;
const string experiment_resutls_path = "results/experiment_rotation2D/";

void read_x(vector<vector<vector<double>>> &x_sets)
{
    stringstream ss;
    ss << setw(3) << setfill('0') << dim;
    string dim_str = ss.str();
    ifstream fin;
    fin.open("results/samplingX_" + dim_str + "D.txt", ios::in);
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

void read_rotation(double matrix[dim][dim], string file_path, int dim)
{
    ifstream fin;
    cout << file_path << endl;
    fin.open(file_path, ios::in);
    if (!fin)
        perror("Error: Cannot open input file for reading");
    for (int i = 0; i < dim; i++)
    {
        for (int j = 0; j < dim; j++)
        {
            fin >> matrix[i][j];
        }
    }
    fin.close();
}

void experiment(vector<vector<vector<double>>> &x_sets, int problem_id,
                int experiment_id = 0, double subtract_lim = 0.,
                double rotate_lim = 0., double scale_factor = 1.,
                bool isSubstract = false, bool isRotate = false,
                bool isScale = false, string matrix_path = "")
{
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
    auto problem = problem_factory.create(problem_id, 1, dim);
    vector<vector<double>> y_sets;
    double rotation_matrix[dim][dim];
    if (isRotate)
        read_rotation(rotation_matrix, matrix_path, 10);
    for (int i = 0; i < num_sampling; i++)
    {
        vector<double> y;
        for (size_t j = 0; j < num_x; j++)
        {
            vector<double> tempx(x_sets[i][j]);
            if (isSubstract)
            {
                vector<double> offset;
                for (int k = 0; k < dim; k++)
                    offset.push_back((rand() / double(RAND_MAX) * 200. - 100.) *
                                     subtract_lim / 100.);
                subtract(tempx, offset);
            }
            if (isRotate)
            {
                vector<double> cacheX(tempx);
                for (int m = 0; m < dim; m++)
                {
                    tempx.at(m) = 0;
                    for (int n = 0; n < dim; n++)
                    {
                        tempx.at(m) =
                            tempx.at(m) + cacheX.at(n) * rotation_matrix[m][n];
                    }
                }
            }
            if (isScale)
            {
                for (int k = 0; k < dim; k++)
                    tempx[k] = tempx[k] * scale_factor;
            }
            double res = (*problem)(tempx);
            y.push_back(res);
        }
        y_sets.push_back(y);
    }
    ofstream fout;
    stringstream ss;
    ss << experiment_resutls_path << to_string(problem_id) << "_"
       << to_string(experiment_id) << "_" << to_string(subtract_lim) << "_"
       << to_string(rotate_lim) << "_" << to_string(scale_factor) << "_"
       << to_string(isSubstract) << "_" << to_string(isRotate) << "_"
       << to_string(isScale) << ".txt";
    fout.open(ss.str(), ios::out);
    for (size_t i = 0; i < y_sets.size(); i++)
    {
        for (size_t j = 0; j < y_sets[i].size(); j++)
        {
            fout << y_sets[i][j] << " ";
        }
        fout << endl;
    }
    fout.close();
}


int main()
{
    // CecUtils cec_utils;
    // vector<vector<vector<double>>> x_sets;
    // read_x(x_sets);

    // vector<string> matrix_path;
    // for (int i = 0; i < 30; i++)
    // {
    //     stringstream ss;
    //     ss << setw(2) << setfill('0') << i;
    //     string num_str = ss.str();
    //     string path =
    //         "results/rotation_matrix/2D/rotation_matrix_" + num_str + ".txt";
    //     matrix_path.push_back(path);
    // }

    // for (int problem_id = 2; problem_id <= 5; problem_id++)
    // {
    //     experiment(x_sets, problem_id);
    //     for (int matrix_ind = 0; matrix_ind < matrix_path.size();
    //     matrix_ind++)
    //     {
    //         experiment(x_sets, problem_id, 0, 0.0, matrix_ind, 1.0, false,
    //         true,
    //                    false, matrix_path[matrix_ind]);
    //     }
    // }
    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        std::string filename =
            "results/landscape/F" + std::to_string(problem_id) + ".txt";
        std::ofstream file(filename);
        if (!file.is_open())
        {
            std::cerr << "Error: could not open file " << filename << std::endl;
            return 1;
        }
        const auto &problem_factory =
            ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
        auto problem = problem_factory.create(problem_id, 1, 2);
        for (double x1 = -100.0; x1 <= 100.0; x1 += 0.5)
        {
            for (double x2 = -100.0; x2 <= 100.0; x2 += 0.5)
            {
                file << x1 << " " << x2 << " " << (*problem)({x1, x2})
                     << std::endl;
            }
        }
    }
}
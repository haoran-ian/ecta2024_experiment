// #include "ioh.hpp"

// using namespace std;
// using namespace ioh::problem::cec;
// using namespace ioh::problem::transformation::objective;
// using namespace ioh::problem::transformation::variables;

// const int num_sampling = 100;
// const int num_x = 1000;
// const int dim = 10;

// void read_x(vector<vector<vector<double>>> &x_sets)
// {
//     stringstream ss;
//     ss << setw(3) << setfill('0') << dim;
//     string dim_str = ss.str();
//     ifstream fin;
//     fin.open("config/samplingX_" + dim_str + "D.txt", ios::in);
//     double read_cache;
//     string header;
//     for (int i = 0; i < num_sampling; i++)
//     {
//         for (int j = 0; j < dim; j++)
//             fin >> header;
//         vector<vector<double>> x;
//         for (int j = 0; j < num_x; j++)
//         {
//             fin >> header;
//             vector<double> x_cache;
//             for (int k = 0; k < dim; k++)
//             {
//                 fin >> read_cache;
//                 x_cache.push_back(read_cache);
//             }
//             x.push_back(x_cache);
//         }
//         x_sets.push_back(x);
//     }
//     fin.close();
// }

// // , double rvec[dim][dim]
// void x_affine(vector<double> &x, vector<double> tvec)
// {
//     for (int i = 0; i < dim; i++)
//         x[i] += tvec[i];
// }

// int main()
// {
//     vector<vector<vector<double>>> x_sets;
//     read_x(x_sets);
//     std::string tvec_filepath = "config/tvec.txt";
//     std::ifstream tvec_file(tvec_filepath);
//     vector<vector<double>> tvecs;
//     for (int i = 0; i < 1000; i++)
//     {
//         vector<double> temp_tvec;
//         for (int j = 0; j < 10; j++)
//         {
//             double t;
//             tvec_file >> t;
//             temp_tvec.push_back(t);
//         }
//         tvecs.push_back(temp_tvec);
//     }
//     for (int problem_id = 1; problem_id <= 5; problem_id++)
//     {
//         const auto &problem_factory =
//             ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
//         auto problem = problem_factory.create(problem_id, 1, dim);
//         for (int i = 0; i < 200; i++)
//         {
//             std::string filename = "data/x_translation/" +
//                                    std::to_string(problem_id) + "_" +
//                                    std::to_string(i) + ".txt";
//             std::ofstream file(filename);
//             vector<double> tvec;
//             tvec = tvecs[i];
//             for (int j = 0; j < 100; j++)
//             {
//                 for (int k = 0; k < 1000; k++)
//                 {
//                     vector<double> x(x_sets[j][k]);
//                     x_affine(x, tvec);
//                     file << (*problem)(x) << " ";
//                 }
//                 file << endl;
//             }
//             file.close();
//         }
//     }
// }
#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;
using namespace ioh::problem::transformation::objective;
using namespace ioh::problem::transformation::variables;

const int num_sampling = 100;
const int num_x = 1000;
const int dim = 10;

void read_x(vector<vector<vector<double>>> &x_sets)
{
    ifstream fin;
    fin.open("config/samplingX_010D.txt", ios::in);
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

void experiment(vector<vector<vector<double>>> &x_sets,
                int problem_id, double subtract_lim)
{
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
    auto problem = problem_factory.create(problem_id, 1, dim);
    vector<vector<double>> y_sets;
    for (int i = 0; i < num_sampling; i++)
    {
        vector<double> y;
        for (size_t j = 0; j < num_x; j++)
        {
            vector<double> tempx(x_sets[i][j]);
            vector<double> offset;
            for (int i = 0; i < dim; i++)
                offset.push_back((rand() / double(RAND_MAX) * 200. - 100.) *
                                    subtract_lim / 100.);
            subtract(tempx, offset);
            double res = (*problem)(tempx);
            y.push_back(res);
        }
        y_sets.push_back(y);
    }
    ofstream fout;
    stringstream ss;
    ss << "ecta2024_data/x_translation/" << to_string(problem_id) << "_"
       << to_string(subtract_lim) << ".txt";
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
    CecUtils cec_utils;
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);

    vector<double> factors;
    int factor_size = 100;
    for (int i = 0; i < factor_size; i++)
        factors.push_back(i + 1.0);

    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        for (int factor_ind = 0; factor_ind < factors.size(); factor_ind++)
        {
            experiment(x_sets, problem_id, factors[factor_ind]);
        }
    }
}

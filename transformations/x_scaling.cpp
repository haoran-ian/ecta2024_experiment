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

// , double rvec[dim][dim]
void x_affine(vector<double> &x, double scale_factor)
{
    for (int i = 0; i < dim; i++)
        x[i] *= scale_factor;
}

int main()
{
    vector<vector<vector<double>>> x_sets;
    read_x(x_sets);
    for (int problem_id = 1; problem_id <= 5; problem_id++)
    {
        const auto &problem_factory =
            ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
        auto problem = problem_factory.create(problem_id, 1, dim);

        for (double i = -2; i<=2; i += 0.1)
        {
            double K = pow(2, i);
            std::string filename = "data/x_scaling/" +
                                   std::to_string(problem_id) + "_" +
                                   std::to_string(K) + ".txt";
            std::ofstream file(filename);
            for (int j = 0; j < 100; j++)
            {
                for (int k = 0; k < 1000; k++)
                {
                    vector<double> x(x_sets[j][k]);
                    x_affine(x, K);
                    file << (*problem)(x) << " ";
                }
                file << endl;
            }
            file.close();
        }
    }
}
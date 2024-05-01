#include "ioh.hpp"

using namespace std;
using namespace ioh::problem::cec;


void read_matrix(string path, double rotation_matrix[2][2])
{
    ifstream infile;
    infile.open(path, ios::in);
    if (!infile)
        perror("Error: Cannot open input file for reading");
    for (int i = 0; i < 2; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            infile >> rotation_matrix[i][j];
        }
    }
    infile.close();
}

void rotation(double rotation_matrix[2][2], vector<double> &x)
{
    double x1 = x[0];
    double x2 = x[1];
    x[0] = rotation_matrix[0][0] * x1 + rotation_matrix[0][1] * x2;
    x[1] = rotation_matrix[1][0] * x1 + rotation_matrix[1][1] * x2;
}

int main()
{
    int problem_id = 1;
    const auto &problem_factory =
        ioh::problem::ProblemRegistry<ioh::problem::CEC2022>::instance();
    auto problem = problem_factory.create(problem_id, 1, 2);
    for (int i = 0; i < 30; i++)
    {
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        string num_str = ss.str();
        string path =
            "results/rotation_matrix/2D/rotation_matrix_" + num_str + ".txt";
        string result_path =
            "results/exp_data/rotation/F1_rotation2D_" + num_str + ".txt";
        ofstream outfile(result_path, ios::out);
        double rotation_matrix[2][2];
        read_matrix(path, rotation_matrix);
        for (double x1 = -100.; x1 <= 100.; x1 += 0.5)
        {
            for (double x2 = -100.; x2 <= 100.; x2 += 0.5)
            {
                auto x = vector<double>{x1, x2};
                auto x_prime(x);
                rotation(rotation_matrix, x_prime);
                double y = (*problem)(x_prime);
                outfile << x1 << " " << x2 << " " << y << endl;
            }
        }
        outfile.close();
    }
}

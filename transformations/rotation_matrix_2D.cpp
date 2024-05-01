#include <cmath>
#include <fstream>
#include <iomanip> // 用于设置输出格式
#include <iostream>

using namespace std;

const double PI = 3.14159265358979323846;

int main()
{
    const int num_matrices = 30; // 矩阵数量
    const double increment = 12.0; // 每个矩阵的角度增量
    double angle_degrees = 0.0; // 旋转角度，单位为度数

    for (int i = 0; i < num_matrices; i++)
    {
        // 转换为弧度
        double angle_radians = angle_degrees * PI / 180.0;

        // 创建旋转矩阵
        double rotation_matrix[2][2] = {
            {cos(angle_radians), -sin(angle_radians)},
            {sin(angle_radians), cos(angle_radians)}};

        // 将矩阵写入文件
        stringstream ss;
        ss << setw(2) << setfill('0') << i;
        string num_str = ss.str();
        string filename =
            "results/rotation_matrix/2D/rotation_matrix_" + num_str + ".txt";
        ofstream outfile(filename);
        outfile << setprecision(6) << fixed; // 设置输出精度为小数点后6位
        for (int j = 0; j < 2; j++)
        {
            for (int k = 0; k < 2; k++)
            {
                outfile << rotation_matrix[j][k] << " ";
            }
            outfile << endl;
        }
        outfile.close();

        // 更新角度
        angle_degrees += increment;
    }

    return 0;
}

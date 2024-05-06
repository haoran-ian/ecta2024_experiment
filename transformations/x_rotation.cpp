#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <sstream>
#include <iterator>

// Define a type for convenience
using Matrix = std::vector<std::vector<double>>;
using ThreeDimVector = std::vector<Matrix>;

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

    while (std::getline(file, line) && num_matrices < 100)
    {
        if (line.find_first_not_of("0123456789 -.") == std::string::npos && !line.empty())
        {
            std::istringstream iss(line);
            std::vector<double> row(std::istream_iterator<double>{iss}, std::istream_iterator<double>());

            if (row.size() == 10)
            {
                current_matrix.push_back(row);

                // When a matrix is complete, add it to the 3D vector and reset for the next matrix
                if (current_matrix.size() == 10)
                {
                    matrices.push_back(current_matrix);
                    current_matrix.clear();
                    num_matrices++;
                }
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

    // Output the matrices to verify
    for (const auto &matrix : matrices)
    {
        for (const auto &row : matrix)
        {
            for (double val : row)
            {
                std::cout << val << " ";
            }
            std::cout << std::endl;
        }
        std::cout << "-------------------" << std::endl;
    }

    return 0;
}

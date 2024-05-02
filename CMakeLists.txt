cmake_minimum_required(VERSION 3.22)

project(cec_test)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(EXTERNAL_DIR "/home/ian/ecta/IOHexperimenter/external")

include_directories(${EXTERNAL_DIR}/fmt/include/)
include_directories(${EXTERNAL_DIR}/clutchlog)
include_directories(${EXTERNAL_DIR}/json/include)

find_package(ioh REQUIRED)

add_executable(cec_test transformations/main.cpp)
target_link_libraries(cec_test ioh::ioh)

add_executable(x_translation transformations/x_translation.cpp)
target_link_libraries(x_translation ioh::ioh)

add_executable(x_scaling transformations/x_scaling.cpp)
target_link_libraries(x_scaling ioh::ioh)

add_executable(rotation_matrix transformations/rotation_matrix.cpp)
target_link_libraries(rotation_matrix ioh::ioh)

add_executable(rotation_matrix_2D transformations/rotation_matrix_2D.cpp)
target_link_libraries(rotation_matrix)

add_executable(porb1_rotation2D transformations/porb1_rotation2D.cpp)
target_link_libraries(porb1_rotation2D ioh::ioh)

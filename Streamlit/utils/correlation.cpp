#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <cmath>

namespace py = pybind11;

double correlation(const std::vector<double>& x, const std::vector<double>& y) {
    if (x.size() != y.size() || x.empty()) {
        throw std::invalid_argument("Input arrays must be of equal size and non-empty.");
    }

    size_t n = x.size();
    double sum_x = 0, sum_y = 0, sum_x2 = 0, sum_y2 = 0, sum_xy = 0;
    for (size_t i = 0; i < n; ++i) {
        sum_x += x[i];
        sum_y += y[i];
        sum_x2 += x[i] * x[i];
        sum_y2 += y[i] * y[i];
        sum_xy += x[i] * y[i];
    }

    double numerator = n * sum_xy - sum_x * sum_y;
    double denominator = std::sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y));
    if (denominator == 0) throw std::runtime_error("Division by zero in correlation calculation.");
    return numerator / denominator;
}

PYBIND11_MODULE(correlation, m) {
    m.doc() = "C++ module for calculating Pearson correlation";
    m.def("correlation", &correlation, "Calculate Pearson correlation between two arrays");
}
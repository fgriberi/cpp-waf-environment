/*
 * @file  mathFuncs.h
 * @brief IFold provides the interface to folding service.
 *
 * @author Franco Riberi
 * @email  fgriberi at gmail.com
 *
 * Contents: Header file for fideo providing struct IFold.
 *
 * System:   cpp-waf-environment: Minimal waf script for C++ programs.
 * Language: C++
 *
 * @date March 06, 2017
 *
 * Copyright (C) 2017  Franco Riberi
 *
 * cpp-waf-environment is free software: you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * fideo is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with fideo.  If not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef MATH_FUNCS_H
#define MATH_FUNCS_H

namespace NSMaths
{
    class MathFuncs
    {
    public:

        static double add(double a, double b);

        static double subtract(double a, double b);

        static double multiply(double a, double b);

        static double divide(double a, double b);

        static double mean(double a, double b);
    };
} //end namespace
#endif /* MATH_FUNCS_H */
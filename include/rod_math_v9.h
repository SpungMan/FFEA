// 
//  This file is part of the FFEA simulation package
//  
//  Copyright (c) by the Theory and Development FFEA teams,
//  as they appear in the README.md file. 
// 
//  FFEA is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
// 
//  FFEA is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//  GNU General Public License for more details.
// 
//  You should have received a copy of the GNU General Public License
//  along with FFEA.  If not, see <http://www.gnu.org/licenses/>.
// 
//  To help us fund FFEA development, we humbly ask that you cite 
//  the research papers on the package.
//

/*
 *      rod_math_v9.h
 *	Author: Rob Welch, University of Leeds
 *	Email: py12rw@leeds.ac.uk
 */

#define OUT

#define _USE_MATH_DEFINES // This has to come before including cmath
#include <cmath>
#include <chrono>
#include <iostream>
#include <cstring>
#include "dimensions.h"

namespace rod {

const double boltzmann_constant = 1.3806503e-23;
static const int x = 0;
static const int y = 1;
static const int z = 2;
static const int twist_dimension = 3;
static const int im2 = 0;
static const int im1 = 1;
static const int i = 2;
static const int ip1 = 3;

static const float rod_software_version = 0.3;

// These are just generic vector functions that will be replaced by mat_vec_fns at some point
void print_array(std::string array_name, float array[], int length);
void normalize(float in[3], OUT float out[3]);
float absolute(float in[3]);
void cross_product(float a[3], float b[3], float out[3]);
void get_rotation_matrix(float a[3], float b[3], float rotation_matrix[9]);
void apply_rotation_matrix(float vec[3], float matrix[9], OUT float rotated_vec[3]);
void apply_rotation_matrix_row(float vec[3], float matrix[9], OUT float rotated_vec[3]);
void matmul_3x3_3x3(float a[9], float b[9], OUT float out[9]);

// These are utility functions specific to the math for the rods

void get_p_i(float curr_r[3], float next_r[3], OUT float p_i[3]);
void rodrigues_rotation(float v[3], float k[3], float theta, OUT float v_rot[3]);
float safe_cos(float in);
float get_l_i(float p_i[3], float p_im1[3]);

     /*-----------------------*/
    /* Update Material Frame */
   /*-----------------------*/

void perpendicularize(float m_i[3], float p_i[3], OUT float m_i_prime[3]);
void update_m1_matrix(float m_i[3], float p_i[3], float p_i_prime[3], float m_i_prime[3]);

     /*------------------*/
    /* Compute Energies */
   /*------------------*/

float get_stretch_energy(float k, float p_i[3], float p_i_equil[3]);
void parallel_transport(float m[3], float m_prime[3], float p_im1[3], float p_i[3]);
float get_twist_energy(float beta, float m_i[3], float m_im1[3], float m_i_equil[3], float m_im1_equil[3], float p_im1[3], float p_i[3], float p_im1_equil[3], float p_i_equil[3]);
void get_kb_i(float p_im1[3], float p_i[3], float e_im1_equil[3], float e_i_equil[3], OUT float kb_i[3]);
void get_omega_j_i(float kb_i[3], float n_j[3], float m_j[3], OUT float omega_j_i[2]);
float get_bend_energy(float omega_i_im1[2], float omega_i_im1_equil[2], float B_equil[4]);

float get_bend_energy_from_p(
        float p_im1[3],
        float p_i[3],
        float p_im1_equil[3],
        float p_i_equil[3],
        float n_im1[3],
        float m_im1[3],
        float n_im1_equil[3],
        float m_im1_equil[3],
        float n_i[3],
        float m_i[3],
        float n_i_equil[3],
        float m_i_equil[3],
        float B_i_equil[4],
        float B_im1_equil[4]);
        
float get_bend_energy_mutual_parallel_transport(
        float p_im1[3],
        float p_i[3],
        float p_im1_equil[3],
        float p_i_equil[3],
        float n_im1[3],
        float m_im1[3],
        float n_im1_equil[3],
        float m_im1_equil[3],
        float n_i[3],
        float m_i[3],
        float n_i_equil[3],
        float m_i_equil[3],
        float B_i_equil[4],
        float B_im1_equil[4]);

     /*----------*/
    /* Dynamics */
   /*----------*/

float get_translational_friction(float viscosity, float radius, bool rotational);
float get_rotational_friction(float viscosity, float radius, float length, bool safe);
float get_force(float bend_energy, float stretch_energy, float delta_x);
float get_torque(float twist_energy, float delta_theta);
float get_delta_r(float friction, float timestep, float force, float noise, float external_force);
float get_noise(float timestep, float kT, float friction, float random_number);

     /*------------*/
    /* Shorthands */
   /*------------*/

void load_p(float p[4][3], float *r, int offset);
void load_m(float m_loaded[4][3], float *m, int offset);
void normalize_all(float p[4][3]);
void absolute_all(float p[4][3], float absolutes[4]);
void cross_all(float p[4][3], float m[4][3], OUT float n[4][3]);
void delta_e_all(float e[4][3], float new_e[4][3], OUT float delta_e[4][3]);
void update_m1_all(float m[4][3], float absolutes[4], float t[4][3], float delta_e[4][3], OUT float m_out[4][3]);
void update_m1_matrix_all(float m[4][3], float p[4][3], float p_prime[4][3], OUT float m_prime[4][3], int start_cutoff, int end_cutoff);
void fix_m1_all(float m[4][3], float new_t[4][3]);
void update_and_fix_m1_all(float old_e[4][3], float new_e[4][3], float m[4][3]);
void set_cutoff_values(int e_i_node_no, int length, OUT int start_cutoff, int end_cutoff);

     /*----------*/
    /* Utility  */
   /*----------*/
   
bool not_simulation_destroying(float x);
bool not_simulation_destroying(float x[3]);
void load_B_all(float B[4][4], float *B_matrix, int offset);
void make_diagonal_B_matrix(float B, OUT float B_matrix[4]);
void set_cutoff_values(int e_i_node_no, int length, OUT int *start_cutoff, int *end_cutoff);
float get_absolute_length_from_array(float* array, int node_no, int length);
void get_centroid(float* r, int length, OUT float centroid[3]);

     /*-------------------------------*/
    /* Move the node, get the energy */
   /*-------------------------------*/

void get_perturbation_energy(
        float perturbation_amount,
        int perturbation_dimension,
        float B_equil[4],
        float *material_params,
        int start_cutoff,
        int end_cutoff,
        int p_i_node_no,
        float *r_all,
        float *r_all_equil,
        float *m_all,
        float *m_all_equil,
        float energies[3]
);

}

from package import generate_makefile

UTILS = {
    "name": "ssl_utils",
    "type": "lib",
    "out": ".",
    "path": "ssl/utilities",
    "sources": [
        "*.c"
    ],
    "includes": ["include"]
}

MD5 = {
    "name": "md5",
    "type": "lib",
    "out": ".",
    "path": "hash/md5",
    "sources": [
        "calculate_md5_block.c",
		"calculate_md5_buf_padding.c",
		"calculate_md5_from_fd.c",
		"calculate_md5_from_string.c",
		"md5.c",
		"print_md5.c",
		"calculate_md5_from_mem.c"
    ],
    "includes": ["include"]
}

SHA256 = {
    "name": "sha256",
    "type": "lib",
    "out": ".",
    "path": "hash/sha256",
    "sources": [
        "calc_sha256_buf_padding.c",
		"calc_sha256_from_fd.c",
		"calc_sha256_from_string.c",
		"print_sha256.c",
		"sha256.c"
    ],
    "includes": ["include"]
}

BASE64 = {
    "name": "base64",
    "type": "lib",
    "out": ".",
    "path": "encode/base64",
    "sources": [
        "base64.c",
        "base64_decode.c",
        "base64_encode.c"
    ],
    "includes": ["include"]
}

ENCODE_CONTEXT = {
    "name": "encode_ctx",
    "type": "lib",
    "out": ".",
    "path": "encode/context",
    "sources": [
        "init_encode_context.c",
		"set_decode_mode.c",
		"set_encode_mode.c",
		"set_input_file.c",
		"set_output_file.c",
		"parse_encode_argv.c",
		"encode_argv_states.c",
        "argv_errors.c",
		"destruct_encode_context.c"
    ],
    "includes": ["include"]
}

ENCODE = {
    "name": "encode",
    "type": "lib",
    "out": ".",
    "path": "encode",
    "sources": ["encode_usage.c"],
    "includes": ["include"],
    "peerdirs": [BASE64, ENCODE_CONTEXT]
}

CIPHER_DES = {
    "name": "cipher_des",
    "type": "lib",
    "out": ".",
    "path": "cipher/des",
    "sources": [
        "des_ecb.c",
		"des_cbc.c",
		"des_cbc_encrypt.c",
		"des_cbc_decrypt.c",
		"des_ecb_encrypt.c",
		"des_ecb_decrypt.c",
        "des_get_block.c",
		"des_key_gen.c",
		"des_encode_block.c",
        "des_permutation.c",
		"des_swap_block_halves.c",
        "try_get_des_salt_from_fd.c",
		"s_permutation.c",
        "des.c",
		"des_cut_padding.c"
    ],
    "includes": ["include"]
}

CIPHER_CONTEXT = {
    "name": "cipher_ctx",
    "type": "lib",
    "out": ".",
    "path": "cipher/context",
    "sources": [
        "cphr_is_a_flag.c",
		"cphr_is_decrypt_mode.c",
		"cphr_is_encrypt_mode.c",
		"cphr_is_iv_set.c",
		"cphr_is_key_set.c",
		"cphr_is_pass_set.c",
		"cphr_is_salt_set.c",
		"cphr_argv_state_a.c",
		"cphr_argv_state_d.c",
		"cphr_argv_state_e.c",
		"cphr_argv_state_i.c",
		"cphr_argv_state_k.c",
		"cphr_argv_state_o.c",
		"cphr_argv_state_p.c",
		"cphr_argv_state_s.c",
		"cphr_argv_state_v.c",
        "set_cipher_init_vector.c",
		"set_cipher_password_from_stdin.c",
		"set_cipher_random_pass_salt.c",
        "set_cipher_pass_salt.c",
		"destruct_cipher_context.c",
        "set_cipher_key.c",
        "set_cipher_bufsize.c",
        "des_argv_states.c",
		"init_cipher_context.c",
		"set_cipher_input_file.c",
		"set_cipher_output_file.c"
    ],
    "includes": ["include"]
}

CIPHER_PBKDF = {
    "name": "cipher_pbkdf",
    "type": "lib",
    "out": ".",
    "path": "cipher/pbkdf",
    "sources": ["pbkdf_md5.c"],
    "includes": ["include"]
}

CIPHER = {
    "type": "lib",
    "name": "cipher",
    "out": ".",
    "path": "ssl",
    "sources": ["cipher_executor.c"],
    "includes": ["include"],
    "peerdirs": [CIPHER_CONTEXT, CIPHER_DES, CIPHER_PBKDF]
}

SSL = {
    "name": "ft_ssl",
    "out": ".",
    "type": "prog",
    "path": "ssl",
    "sources": [
        "command_executor.c",
		"hash_executor.c",
		"help.c",
		"main.c",
		"parse_hash_flags.c",
		"encode_executor.c",
		"wrong_command_exit.c"
    ],
    "peerdirs": [UTILS, CIPHER, ENCODE, MD5, SHA256],
    "includes": ["include"]
}

COMPILERS = {
    "c": {
        "flags": "",
        "file_extension": "c",
        "std": "-std=c99",
        "binary": "clang",
    }
}

generate_makefile(SSL, COMPILERS)
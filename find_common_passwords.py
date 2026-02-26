import hashlib

# Check what password generates the common hash
common_hash = '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92'

# Try common passwords
passwords_to_try = [
    'password', '123456', 'admin', 'test', 'user', 'resident', 
    'mamamo', 'abudul', 'papamo', 'kuyako', 'abdulhalal', 'mamamoko',
    'zepol052904', 'leo', 'resident1', 'barangay', '1234', 'qwerty'
]

print(f'🔍 Looking for password that generates: {common_hash}')

for password in passwords_to_try:
    test_hash = hashlib.sha256(password.encode()).hexdigest()
    if test_hash == common_hash:
        print(f'✅ FOUND PASSWORD: "{password}"')
        break
else:
    print('❌ No common password matches found')

# Also check the unresident hash
unresident_hash = '2e5b8f6b5561f7aee910484b6d84c9be23247e8cc76999965556a9d622b96e0b'
print(f'\n🔍 Looking for password that generates: {unresident_hash}')

for password in passwords_to_try:
    test_hash = hashlib.sha256(password.encode()).hexdigest()
    if test_hash == unresident_hash:
        print(f'✅ FOUND PASSWORD for unresident: "{password}"')
        break
else:
    print('❌ No common password matches found for unresident')

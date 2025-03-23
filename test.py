import utilities


model=utilities.getconfig()['embedmodel']
print(model)

print("\n\n")

files_dict = utilities.readtext("docs_for_test/")
# Print first 2 lines of each file
for filename, content in files_dict.items():
    print(f"\nFile: {filename}")
    print("First 2 lines:")
    print('\n'.join(content.splitlines()[:2]))
    print("-" * 50)
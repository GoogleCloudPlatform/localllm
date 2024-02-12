from LocalQueryRunner.querylocal import RunLocalQuey

runner = RunLocalQuey()
while True:
    user_input = input("<user> ")
    response = runner.get_response(prompt=user_input)
    print(f"\n<model> {response}")
response ={
    'messages': [
        HumanMessage(
            content='what is the weather outside?', 
            additional_kwargs={}, 
            response_metadata={}, 
            id='b930df6f-b15e-4169-a985-f8a4b3bc3d37'), 
        AIMessage(
            content='', 
            additional_kwargs={
                'tool_calls': [{
                    'id': 'call_abc7ae1dbe66487584d38b', 
                    'function': {'arguments': '{}', 'name': 'get_user_location'}, 
                    'type': 'function', 
                    'index': 0}],
                'refusal': None}, 
            response_metadata={
                'token_usage': {
                    'completion_tokens': 13, 
                    'prompt_tokens': 322, 
                    'total_tokens': 335, 
                    'completion_tokens_details': None, 
                    'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 256}}, 
                'model_name': 'qwen-flash', 
                'system_fingerprint': None, 
                'id': 'chatcmpl-171b6876-6b9a-937f-9b10-5c18e21876e8', 
                'service_tier': None, 
                'finish_reason': 'tool_calls', 
                'logprobs': None}, 
            id='lc_run--019d1922-0e72-7322-81cd-3c4a7b38777a-0', 
            tool_calls=[{
                'name': 'get_user_location', 
                'args': {}, 
                'id': 'call_abc7ae1dbe66487584d38b', 
                'type': 'tool_call'}], 
            invalid_tool_calls=[], 
            usage_metadata={
                'input_tokens': 322, 
                'output_tokens': 13, 
                'total_tokens': 335, 
                'input_token_details': {'cache_read': 256}, 
                'output_token_details': {}}), 
        ToolMessage(
            content='xian', 
            name='get_user_location', 
            id='5160964a-0464-43be-b816-537ef4d5bb17', 
            tool_call_id='call_abc7ae1dbe66487584d38b'), 
        AIMessage(
            content='', 
            additional_kwargs={
                'tool_calls': [{
                    'id': 'call_713e257fb58b426c9a0da7', 
                    'function': {'arguments': '{"city": "xian"}', 'name': 'get_weather'}, 
                    'type': 'function', 
                    'index': 0}], 
                'refusal': None}, 
            response_metadata={
                'token_usage': {
                    'completion_tokens': 17, 
                    'prompt_tokens': 354, 
                    'total_tokens': 371, 
                    'completion_tokens_details': None, 
                    'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 256}}, 
                'model_name': 'qwen-flash', 
                'system_fingerprint': None, 
                'id': 'chatcmpl-398e2025-2e04-9c2f-a2d9-3337abf25120', 
                'service_tier': None, 
                'finish_reason': 'tool_calls', 
                'logprobs': None}, 
            id='lc_run--019d1922-120e-7d23-97f1-8abef8ebea2e-0', 
            tool_calls=[{
                'name': 'get_weather', 
                'args': {'city': 'xian'}, 
                'id': 'call_713e257fb58b426c9a0da7', 
                'type': 'tool_call'}], 
            invalid_tool_calls=[], 
            usage_metadata={
                'input_tokens': 354, 
                'output_tokens': 17, 
                'total_tokens': 371, 
                'input_token_details': {'cache_read': 256}, 'output_token_details': {}}), 
        ToolMessage(
            content="It's always sunny in xian!", 
            name='get_weather', 
            id='c706c2dd-f184-4dd8-946e-81f8d3007789', 
            tool_call_id='call_713e257fb58b426c9a0da7'), 
        AIMessage(
            content='', 
            additional_kwargs={
                'tool_calls': [{
                    'id': 'call_e5f83649a5644064ae77fc', 
                    'function': {
                        'arguments': '{"punny_response": "It\'s always sunny in xian! 😎", "weather_conditions": "sunny"}', 
                        'name': 'ResponseFormat'}, 
                    'type': 'function', 
                    'index': 0}], 
                'refusal': None}, 
            response_metadata={
                'token_usage': {
                    'completion_tokens': 35, 
                    'prompt_tokens': 395, 
                    'total_tokens': 430, 
                    'completion_tokens_details': None, 
                    'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 
                'model_name': 'qwen-flash', 
                'system_fingerprint': None, 
                'id': 'chatcmpl-5cf90bb0-3ec8-9725-89f5-a6e40a022ebb', 
                'service_tier': None, 
                'finish_reason': 'tool_calls', 
                'logprobs': None}, 
            id='lc_run--019d1922-13ef-7bd3-af4e-77f5b6463c87-0', 
            tool_calls=[{
                'name': 'ResponseFormat', 
                'args': {'punny_response': "It's always sunny in xian! 😎", 'weather_conditions': 'sunny'}, 
                'id': 'call_e5f83649a5644064ae77fc', 
                'type': 'tool_call'}], 
            invalid_tool_calls=[], 
            usage_metadata={
                'input_tokens': 395, 
                'output_tokens': 35, 
                'total_tokens': 430, 
                'input_token_details': {'cache_read': 0}, 
                'output_token_details': {}}), 
        ToolMessage(
            content='Returning structured response: ResponseFormat(punny_response="It\'s always sunny in xian! 😎", weather_conditions=\'sunny\')', 
            name='ResponseFormat', 
            id='8a5dc064-c9a3-4d1c-b474-ce1a2899e670', 
            tool_call_id='call_e5f83649a5644064ae77fc')], 
    'structured_response': ResponseFormat(punny_response="It's always sunny in xian! 😎", weather_conditions='sunny')}
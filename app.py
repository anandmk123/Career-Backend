from flask import Flask, request, jsonify
from flask_cors import CORS
import matlab.engine

app = Flask(__name__)

CORS(app)


# Start MATLAB engine
eng = matlab.engine.start_matlab()

# Define the career group names in the correct order
career_groups = [
    "Engineering_Tech",          # Output 1
    "Healthcare_Medicine",       # Output 2
    "Business_Commerce",         # Output 3
    "Creative_Arts_Design",      # Output 4
    "Sports_Physical_Edu",       # Output 5
    "Teaching_Social_Services"   # Output 6
]

@app.route('/recommend', methods=['GET'])
def recommend():
    try:
        # Extract input variables from query parameters
        inputs = [
            float(request.args.get('Physics', 0)),
            float(request.args.get('Chemistry', 0)),
            float(request.args.get('Mathematics', 0)),
            float(request.args.get('Biology', 0)),
            float(request.args.get('English', 0)),
            float(request.args.get('SocialScience', 0)),
            float(request.args.get('LogicalThinking', 0)),
            float(request.args.get('CreativeThinking', 0)),
            float(request.args.get('Leadership', 0)),
            float(request.args.get('Volunteering', 0)),
            float(request.args.get('Sports', 0)),
            float(request.args.get('Arts', 0)),
            float(request.args.get('ScienceClub', 0)),
            float(request.args.get('NCC_NSS', 0))
        ]

        # Convert inputs to MATLAB array
        matlab_inputs = matlab.double(inputs)

        # Load the .fis file (replace 'CareerRecommendation_trapz.fis' with your file)
        fis = eng.readfis('CareerRecommendation_trapz.fis')

        # Evaluate the FIS
        output = eng.evalfis(fis, matlab_inputs)

        # Convert MATLAB output to a Python list
        output = list(output[0])  # Extract the first element (matlab.double) and convert to list
        print("Converted output:", output)

        # Ensure the output has exactly 6 values
        if len(output) != len(career_groups):
            raise ValueError(f"Expected {len(career_groups)} output values, but got {len(output)}")

        # Prepare the response by mapping output values to career groups
        response = {
            career_groups[i]: output[i] for i in range(len(career_groups))
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
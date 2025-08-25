#version 330 core
in vec3 vColor;
in vec3 vNormal;
in vec3 vWorld;

uniform vec3 uViewPos;
out vec4 FragColor;

void main(){
    vec3 N = normalize(vNormal);
    vec3 L = normalize(vec3(0.6, 1.0, 0.4));  // sun dir
    float diff = max(dot(N, L), 0.0);
    float amb = 0.35;
    vec3 col = vColor * (amb + diff * 0.8);

    // mild distance fog
    float d = distance(uViewPos, vWorld);
    float fog = clamp((d-40.0)/80.0, 0.0, 1.0);
    vec3 sky = vec3(0.65, 0.80, 1.0);
    col = mix(col, sky, fog);

    FragColor = vec4(col, 1.0);
}

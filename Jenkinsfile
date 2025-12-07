pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo '☁️ Obteniendo código...'
                checkout scm
            }
        }

        stage('SCA - Safety') {
            steps {
                script {
                    echo '🔍 Ejecutando SCA...'
                    sh 'pip3 install safety --break-system-packages'
                    
                    // Ejecutamos Safety. Si encuentra fallos, devuelve error (exit code 1)
                    // Guardamos la salida en un archivo de texto
                    def exitCode = sh(script: 'safety check -r app/requirements.txt > safety_report.txt', returnStatus: true)
                    
                    // Importante: Guardar el reporte SIEMPRE, pase o falle
                    archiveArtifacts artifacts: 'safety_report.txt', allowEmptyArchive: true
                    
                    if (exitCode != 0) {
                        error("❌ SCA FALLÓ: Se detectaron librerías vulnerables. El pipeline se detiene aquí.")
                    } else {
                        echo "✅ SCA Aprobado."
                    }
                }
            }
        }

        stage('SAST - Bandit') {
            steps {
                script {
                    echo '🔍 Ejecutando SAST...'
                    sh 'pip3 install bandit --break-system-packages'
                    
                    // Ejecutamos Bandit.
                    def exitCode = sh(script: 'bandit -r app/ -f json -o bandit_report.json', returnStatus: true)
                    
                    archiveArtifacts artifacts: 'bandit_report.json', allowEmptyArchive: true
                    
                    if (exitCode != 0) {
                        error("❌ SAST FALLÓ: Se detectó código inseguro. El pipeline se detiene aquí.")
                    } else {
                        echo "✅ SAST Aprobado."
                    }
                }
            }
        }

        stage('DAST - OWASP ZAP') {
            steps {
                script {
                    echo '🚀 Desplegando App para DAST...'
                    // Limpieza previa
                    sh 'docker rm -f target-app zap-run || true'
                    
                    // Construir y correr la app
                    sh 'docker build -t target-app app/'
                    sh 'docker run -d --name target-app -p 5000:5000 target-app'
                    
                    sleep 10 

                    echo '⚔️ Ejecutando ZAP...'
                    // Usamos volumen anónimo para evitar problemas de permisos
                    try {
                        sh 'docker run --name zap-run -u 0 -v /zap/wrk zaproxy/zap-stable zap-baseline.py -t http://172.17.0.1:5000 -r zap_report.html || true'
                    } catch (Exception e) {
                        echo 'ZAP finalizó con alertas.'
                    }
                    
                    echo '📄 Extrayendo reporte ZAP...'
                    sh 'docker cp zap-run:/zap/wrk/zap_report.html .'
                    archiveArtifacts artifacts: 'zap_report.html', allowEmptyArchive: true
                    
                    // Limpieza final
                    sh 'docker rm -f zap-run target-app'
                }
            }
        }
    }
}

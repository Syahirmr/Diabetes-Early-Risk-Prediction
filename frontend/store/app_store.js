import landingHtml from '../pages/landing.html?raw';
import assessmentHtml from '../pages/assessment.html?raw';
import resultHtml from '../pages/result.html?raw';
import explanationHtml from '../components/explanation_panel.html?raw';

export function appStore() {
    return {
        step: 'landing', // landing, assessment, result
        apiStatus: 'checking',
        loading: false,
        error: null,
        
        assessment: {
            age: '',
            gender: '',
            bmi: '',
            hypertension: '',
            heart_disease: '',
            smoking_history: '',
            hba1c_level: '',
            blood_glucose_level: ''
        },
        
        resultData: null,
        explainData: null,
        explainLoading: false,
        
        pages: {
            landing: landingHtml,
            assessment: assessmentHtml,
            result: resultHtml
        },
        
        components: {
            explanation: explanationHtml
        },

        async init() {
            // Check API Health non-blocking
            this.checkHealth();

            // Restore state from sessionStorage
            const savedAssessment = sessionStorage.getItem('draft_assessment');
            if (savedAssessment) {
                try {
                    this.assessment = JSON.parse(savedAssessment);
                } catch(e) {}
            }
            
            // Auto-save on change
            this.$watch('assessment', (val) => {
                sessionStorage.setItem('draft_assessment', JSON.stringify(val));
            });

            // Handle Initial Routing
            if(window.location.hash) {
                const hashStep = window.location.hash.substring(1);
                if(['landing', 'assessment', 'result'].includes(hashStep)) {
                    this.step = hashStep;
                } else {
                    this.step = 'landing';
                    history.replaceState({step: 'landing'}, '', '/');
                }
            } else {
                history.replaceState({step: this.step}, '', '/');
            }

            // Restore state if any popstate
            window.addEventListener('popstate', (e) => {
                if(e.state && e.state.step) {
                    this.step = e.state.step;
                } else if(window.location.hash) {
                    const hashStep = window.location.hash.substring(1);
                    if(['landing', 'assessment', 'result'].includes(hashStep)) {
                        this.step = hashStep;
                    }
                }
            });
        },
        
        async checkHealth() {
            try {
                await window.apiClient.health();
                this.apiStatus = 'ok';
            } catch(e) {
                this.apiStatus = 'error';
                this.error = "Gagal terhubung ke server backend.";
            }
        },
        
        goTo(newStep) {
            this.step = newStep;
            history.pushState({step: newStep}, '', '/' + (newStep === 'landing' ? '' : '#' + newStep));
            window.scrollTo(0,0);
        },
        
        async submitAssessment() {
            this.loading = true;
            this.error = null;
            this.explainData = null; // reset explanation
            
            const payload = {
                age: Number(this.assessment.age),
                gender: this.assessment.gender,
                bmi: Number(this.assessment.bmi),
                hypertension: Number(this.assessment.hypertension),
                heart_disease: Number(this.assessment.heart_disease),
                smoking_history: this.assessment.smoking_history,
                hba1c_level: Number(this.assessment.hba1c_level),
                blood_glucose_level: Number(this.assessment.blood_glucose_level)
            };
            
            try {
                this.resultData = await window.apiClient.predict(payload);
                this.goTo('result');
            } catch(e) {
                if(e.message !== 'Request dibatalkan.') {
                    this.error = e.message;
                }
            } finally {
                this.loading = false;
            }
        },
        
        async loadExplain() {
            if (this.explainData || this.explainLoading) return;
            this.explainLoading = true;
            const payload = {
                age: Number(this.assessment.age),
                gender: this.assessment.gender,
                bmi: Number(this.assessment.bmi),
                hypertension: Number(this.assessment.hypertension),
                heart_disease: Number(this.assessment.heart_disease),
                smoking_history: this.assessment.smoking_history,
                hba1c_level: Number(this.assessment.hba1c_level),
                blood_glucose_level: Number(this.assessment.blood_glucose_level)
            };
            try {
                this.explainData = await window.apiClient.explain(payload);
            } catch(e) {
                if(e.message !== 'Request dibatalkan.') {
                    this.error = "Gagal memuat explainability: " + e.message;
                }
            } finally {
                this.explainLoading = false;
            }
        },
        
        printResult() {
            window.print();
        }
    };
}

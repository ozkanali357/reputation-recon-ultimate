import React, { useState, useEffect } from 'react';
import { Search, Shield, Database, GitCompare, Loader2, ExternalLink } from 'lucide-react';

export default function WithSecureAssessor() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [assessment, setAssessment] = useState(null);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/history');
      const data = await response.json();
      setHistory(data);
    } catch (error) {
      console.error('Failed to fetch history:', error);
    }
  };

  const runAssessment = async () => {
    if (!input.trim()) return;
    
    setLoading(true);
    setError(null);
    setAssessment(null);

    try {
      const response = await fetch('http://localhost:5000/api/assess', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: input.trim(),
          snapshot_mode: true
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setAssessment(data);
      fetchHistory();
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-3">
            <Shield className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              Reputation Recon Ultimate
            </h1>
          </div>
          <p className="text-gray-400">Powered by WithSecure Evidence Engine</p>
        </div>

        {/* Search Bar */}
        <div className="bg-slate-800 rounded-lg p-6 shadow-xl border border-slate-700 mb-6">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && runAssessment()}
                placeholder="Enter product name, URL, or SHA1..."
                className="w-full pl-10 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500"
              />
            </div>
            <button
              onClick={runAssessment}
              disabled={loading || !input.trim()}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Assessing...
                </>
              ) : (
                <>
                  <Shield className="w-5 h-5" />
                  Assess
                </>
              )}
            </button>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-900/20 border border-red-700 rounded-lg p-4 mb-6">
            <p className="text-red-300">Error: {error}</p>
          </div>
        )}

        {/* Assessment Results */}
        {assessment && (
          <div className="space-y-6">
            {/* Entity Info */}
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-white mb-1">
                    {assessment.entity.product_name}
                  </h2>
                  <p className="text-gray-400">by {assessment.entity.vendor}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    Category: {assessment.taxonomy} • Confidence: {Math.round(assessment.entity.confidence * 100)}%
                  </p>
                </div>
                <div className="text-right">
                  <div className={`text-4xl font-bold mb-1 ${
                    assessment.trust_score.value >= 80 ? 'text-green-400' :
                    assessment.trust_score.value >= 60 ? 'text-yellow-400' :
                    'text-red-400'
                  }`}>
                    {assessment.trust_score.value}
                  </div>
                  <p className="text-sm text-gray-400">Trust Score</p>
                  <p className="text-xs text-gray-500 mt-1">
                    {assessment.trust_score.confidence} confidence
                  </p>
                </div>
              </div>

              <p className="text-sm text-gray-300 bg-slate-700 rounded p-3">
                {assessment.trust_score.rationale}
              </p>
            </div>

            {/* Security Brief */}
            {assessment.brief && (
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <Database className="w-5 h-5 text-blue-400" />
                  Security Posture Brief
                </h3>

                <div className="space-y-4">
                  {/* Description */}
                  <div>
                    <h4 className="font-semibold text-blue-300 mb-2">Description & Usage</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{assessment.brief.description}</p>
                    <p className="text-gray-400 text-sm leading-relaxed mt-1">{assessment.brief.usage}</p>
                  </div>

                  {/* Vendor Reputation */}
                  <div className="pt-4 border-t border-slate-700">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-semibold text-blue-300">Vendor Reputation</h4>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        assessment.brief.vendorReputation.psirtMaturity === 'HIGH' ? 'bg-green-900/30 text-green-300' :
                        assessment.brief.vendorReputation.psirtMaturity === 'MEDIUM' ? 'bg-yellow-900/30 text-yellow-300' :
                        'bg-red-900/30 text-red-300'
                      }`}>
                        PSIRT: {assessment.brief.vendorReputation.psirtMaturity}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm leading-relaxed">{assessment.brief.vendorReputation.summary}</p>
                  </div>

                  {/* Vulnerability Trends */}
                  <div className="pt-4 border-t border-slate-700">
                    <h4 className="font-semibold text-blue-300 mb-2">Vulnerability Trends</h4>
                    <p className="text-gray-300 text-sm leading-relaxed mb-2">{assessment.brief.vulnerabilityTrends.summary}</p>
                    <div className="flex gap-4 text-xs">
                      <span className="text-red-400">Critical: {assessment.brief.vulnerabilityTrends.criticalCount}</span>
                      <span className="text-orange-400">High: {assessment.brief.vulnerabilityTrends.highCount}</span>
                      <span className="text-yellow-400">Medium: {assessment.brief.vulnerabilityTrends.mediumCount}</span>
                    </div>
                  </div>

                  {/* Incidents */}
                  <div className="pt-4 border-t border-slate-700">
                    <h4 className="font-semibold text-blue-300 mb-2 flex items-center gap-2">
                      Incident History
                      {assessment.brief.incidents.hasKEV && (
                        <span className="px-2 py-1 bg-red-900/30 text-red-300 rounded text-xs">
                          ⚠ CISA KEV
                        </span>
                      )}
                    </h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{assessment.brief.incidents.summary}</p>
                  </div>

                  {/* Data Handling */}
                  <div className="pt-4 border-t border-slate-700">
                    <h4 className="font-semibold text-blue-300 mb-2">Data Handling & Compliance</h4>
                    <p className="text-gray-300 text-sm leading-relaxed mb-2">{assessment.brief.dataHandling.summary}</p>
                    <div className="flex gap-2 flex-wrap">
                      {assessment.brief.dataHandling.compliance.map((cert, i) => (
                        <span key={i} className="px-2 py-1 bg-blue-900/30 text-blue-300 rounded text-xs">
                          {cert}
                        </span>
                      ))}
                    </div>
                  </div>

                  {/* Controls */}
                  <div className="pt-4 border-t border-slate-700">
                    <h4 className="font-semibold text-blue-300 mb-2">Security Controls</h4>
                    <p className="text-gray-300 text-sm leading-relaxed">{assessment.brief.controls.summary}</p>
                    <div className="text-xs text-gray-400 mt-2">
                      <span>Access: {assessment.brief.controls.accessControl}</span>
                      <span className="mx-2">•</span>
                      <span>Logging: {assessment.brief.controls.logging}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Trust Score Breakdown */}
            <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
              <h3 className="text-xl font-bold text-white mb-4">Trust Score Breakdown</h3>
              <div className="space-y-3">
                {assessment.trust_score.breakdown.map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-sm text-gray-300">{item.component}</span>
                        <span className="text-sm text-gray-400">{item.score}/100 ({Math.round(item.weight * 100)}%)</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            item.score >= 80 ? 'bg-green-500' :
                            item.score >= 60 ? 'bg-yellow-500' :
                            'bg-red-500'
                          }`}
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Evidence Sources */}
            {assessment.evidence_sources && assessment.evidence_sources.length > 0 && (
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-xl font-bold text-white mb-4">Evidence Sources</h3>
                <div className="space-y-2">
                  {assessment.evidence_sources.map((source, i) => (
                    <div key={i} className="flex items-center justify-between p-3 bg-slate-700 rounded">
                      <div>
                        <p className="text-white font-medium">{source.type}</p>
                        <p className="text-xs text-gray-400">
                          Retrieved: {new Date(source.retrieved_at).toLocaleString()}
                          {source.count && ` • ${source.count} entries`}
                        </p>
                      </div>
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-blue-400 hover:text-blue-300 flex items-center gap-1"
                      >
                        <ExternalLink className="w-4 h-4" />
                      </a>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Alternatives */}
            {assessment.alternatives && assessment.alternatives.length > 0 && (
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <h3 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
                  <GitCompare className="w-5 h-5 text-blue-400" />
                  Safer Alternatives
                </h3>
                <div className="grid gap-4 md:grid-cols-2">
                  {assessment.alternatives.map((alt, i) => (
                    <div key={i} className="p-4 bg-slate-700 rounded-lg border border-slate-600 hover:border-blue-500 transition-colors">
                      <h4 className="font-bold text-white mb-1">{alt.product || alt.name}</h4>
                      <p className="text-sm text-gray-400 mb-2">by {alt.vendor}</p>
                      <p className="text-sm text-gray-300">{alt.rationale || alt.reason}</p>
                      {alt.trust_score && (
                        <div className="mt-2 text-xs text-green-400">
                          Trust Score: {alt.trust_score}/100
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* CVE Details */}
            {assessment.cve_data && assessment.cve_data.length > 0 && (
              <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">Vulnerability Details</h3>
                  <span className="text-sm text-gray-400">
                    Showing {Math.min(5, assessment.cve_data.length)} of {assessment.cve_data.length} CVEs
                  </span>
                </div>
                <div className="space-y-3">
                  {assessment.cve_data.slice(0, 5).map((cve, i) => (
                    <div key={i} className="p-3 bg-slate-700 rounded border-l-4 border-l-yellow-500">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-mono text-blue-300">{cve.id}</span>
                            <span className={`px-2 py-0.5 rounded text-xs ${
                              cve.severity === 'CRITICAL' ? 'bg-red-900/30 text-red-300' :
                              cve.severity === 'HIGH' ? 'bg-orange-900/30 text-orange-300' :
                              'bg-yellow-900/30 text-yellow-300'
                            }`}>
                              {cve.severity} • {cve.score}/10
                            </span>
                          </div>
                          <p className="text-sm text-gray-300">{cve.description}</p>
                          <p className="text-xs text-gray-500 mt-1">Published: {cve.published}</p>
                        </div>
                        <a
                          href={cve.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-400 hover:text-blue-300 ml-3"
                        >
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* History Sidebar */}
        {history.length > 0 && (
          <div className="mt-6 bg-slate-800 rounded-lg p-4 border border-slate-700">
            <h3 className="text-lg font-bold text-white mb-3">Recent Assessments</h3>
            <div className="space-y-2">
              {history.slice(0, 5).map((item, i) => (
                <button
                  key={i}
                  onClick={() => setAssessment(item)}
                  className="w-full text-left p-2 bg-slate-700 hover:bg-slate-600 rounded text-sm transition-colors"
                >
                  <div className="text-white font-medium">{item.entity?.product_name || 'Unknown'}</div>
                  <div className="text-xs text-gray-400">
                    {item.trust_score?.value}/100 • {new Date(item.timestamp).toLocaleString()}
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}